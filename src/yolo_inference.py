#!/usr/bin/env python3
import os
import cv2
import yaml
import time
import json
import torch
import signal
import logging
import sqlite3
import requests
import numpy as np
from ultralytics import YOLO
from typing import List, Tuple, Optional
from deep_sort_realtime.deepsort_tracker import DeepSort
from card_mapper import get_card_name, get_barcode_from_card_id

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")

class HTTPTrackerDetector:
    def __init__(self, config_path: str = "config/settings.yaml") -> None:
        with open(config_path, "r") as file:
            config = yaml.safe_load(file)

        self.http_endpoint = config.get("http_endpoint", "http://localhost:8111/")
        self.confidence_threshold = config.get("confidence_threshold", 0.9)
        self.model_path = config.get("model_path", "models/best.pt")

        self.device = "cuda" if torch.cuda.is_available() else "cpu"  
        self.model = YOLO(self.model_path).to(self.device)
        self.tracker = DeepSort(max_age=60, n_init=2, embedder="mobilenet", half=True, max_iou_distance=0.5)
        self.reported_tracks = set()

        self.stream_id = None
        self.stream_url = None
        self.table_id = None
        self.publish_count = 0
        self.retry_delay = config.get("retry_delay", 30)  

        # Register shutdown hook
        signal.signal(signal.SIGTERM, self.shutdown)
        signal.signal(signal.SIGINT, self.shutdown)

    def perform_detection(self, frame: np.ndarray) -> List[Tuple[List[float], float, int]]:
        results = self.model(frame, imgsz=640, verbose=False, conf=self.confidence_threshold)
        detections = []
        if results and len(results) > 0:
            for box in results[0].boxes:
                conf = float(box.conf[0].item())
                class_id = int(box.cls[0].item())
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                if conf >= self.confidence_threshold:
                    w = x2 - x1
                    h = y2 - y1
                    detections.append(([x1, y1, w, h], conf, class_id))
        return detections

    @staticmethod
    def compute_iou(boxA: List[float], boxB: List[float]) -> float:
        xA = max(boxA[0], boxB[0])
        yA = max(boxA[1], boxB[1])
        xB = min(boxA[2], boxB[2])
        yB = min(boxA[3], boxB[3])
        inter_area = max(0, xB - xA) * max(0, yB - yA)
        if inter_area == 0:
            return 0.0
        boxA_area = (boxA[2] - boxA[0]) * (boxA[3] - boxA[1])
        boxB_area = (boxB[2] - boxB[0]) * (boxB[3] - boxB[1])
        return inter_area / float(boxA_area + boxB_area - inter_area)

    def associate_detection(self, track_bbox: List[float], detections: List[Tuple[List[float], float, int]], iou_threshold: float = 0.3) -> Optional[Tuple[List[float], float, int]]:
        best_det = None
        best_iou = 0.0
        for det in detections:
            bbox_xywh, conf, class_id = det
            det_bbox = [bbox_xywh[0], bbox_xywh[1], bbox_xywh[0] + bbox_xywh[2], bbox_xywh[1] + bbox_xywh[3]]
            iou_val = self.compute_iou(track_bbox, det_bbox)
            if iou_val > best_iou:
                best_iou = iou_val
                best_det = det
        return best_det if best_iou >= iou_threshold else None

    def process_tracks(self, tracks: list, detections: List[Tuple[List[float], float, int]], current_time: int) -> List[dict]:
        new_tracks = []
        for track in tracks:
            if not track.is_confirmed():
                continue
            track_id = track.track_id
            if track_id in self.reported_tracks:
                continue

            track_bbox = track.to_ltrb().tolist()
            associated_det = self.associate_detection(track_bbox, detections, iou_threshold=0.5)
            if associated_det:
                _, conf, class_id = associated_det
            else:
                conf, class_id = None, None

            self.reported_tracks.add(track_id)
            new_tracks.append({
                "track_id": track_id,
                "class_id": class_id,
                "card_name": get_card_name(class_id),
                "barcode": get_barcode_from_card_id(class_id),
                "confidence": conf,
                "bbox": track_bbox,
                "timestamp": current_time
            })
        return new_tracks

    def process_frame(self, frame: np.ndarray) -> None:
        try:
            detections = self.perform_detection(frame)
            tracks = self.tracker.update_tracks(detections, frame=frame)
            now_ts = int(time.time())
            new_tracks = self.process_tracks(tracks, detections, now_ts)
            if new_tracks:
                result_msg = {
                    "stream_id": self.stream_id,
                    "tableId": self.table_id,
                    "detections": new_tracks,
                }
                result_json = json.dumps(result_msg)
                response = requests.post(self.http_endpoint, data=result_json, headers={'Content-Type': 'application/json'})
                if response.status_code == 200:
                    self.publish_count += 1
                    logging.info(f"Published detection results to {self.http_endpoint}. Total published: {self.publish_count}")
                else:
                    logging.error(f"Failed to publish detection results: {response.status_code} {response.text}")
        except Exception as e:
            logging.error("Error processing frame: %s", e, exc_info=True)

    def process_stream(self) -> None:
        os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;tcp"
        cap = cv2.VideoCapture(self.stream_url, cv2.CAP_FFMPEG)
        frame_count = 0
        try:
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                frame_count += 1
                if frame_count % 3 == 0:
                    logging.info("frame processed")
                    self.process_frame(frame)
        except Exception as e:
            logging.error("Error processing stream: %s", e, exc_info=True)
        finally:
            cap.release()
            self.reset_picked()

    def worker(self) -> None:
        while True:
            stream_info = self.pick_stream()
            if stream_info:
                self.stream_id, self.stream_url, self.table_id = stream_info
                self.process_stream()
            else:
                logging.info(f"No available streams to process. Retrying in {self.retry_delay} seconds...")
                time.sleep(self.retry_delay)

    def pick_stream(self) -> Optional[Tuple[int, str, str]]:
        while True:
            conn = sqlite3.connect('config/streams.db')
            cursor = conn.cursor()
            cursor.execute("BEGIN IMMEDIATE")
            cursor.execute("SELECT id, url, tableId FROM streams WHERE picked_for_yolo = 0 LIMIT 1")
            stream = cursor.fetchone()
            if stream:
                stream_id, stream_url, table_id = stream
                cursor.execute("UPDATE streams SET picked_for_yolo = 1 WHERE tableId = ?", (table_id,))
                conn.commit()
                conn.close()
                logging.info(f"Picked stream: id={stream_id}, url={stream_url}, tableId={table_id}")
                return stream_id, stream_url, table_id
            conn.rollback()
            conn.close()
            logging.info(f"No available streams to pick. Retrying in {self.retry_delay} seconds...")
            time.sleep(self.retry_delay)

    def reset_picked(self) -> None:
        if self.table_id:
            conn = sqlite3.connect('config/streams.db')
            cursor = conn.cursor()
            cursor.execute("UPDATE streams SET picked_for_yolo = 0 WHERE tableId = ?", (self.table_id,))
            conn.commit()
            conn.close()

    def shutdown(self, signum, frame) -> None:
        logging.info("Shutting down...")
        self.reset_picked()
        exit(0)

    def run(self) -> None:
        logging.info("HTTPTrackerDetector: Waiting for streams...")
        self.worker()

def main() -> None:
    detector = HTTPTrackerDetector()
    detector.run()

if __name__ == "__main__":
    main()