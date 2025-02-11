# **RTSP Card Detection System (CPU/GPU Version)**
> **Real-time playing card detection from RTSP streams using YOLO, DeepSORT, RabbitMQ, and SQLite.**

## **Overview**
The **RTSP Card Detection System** is a deep-learning-based real-time card detection solution that processes video streams from an RTSP source. The system leverages **YOLO for object detection**, **DeepSORT for object tracking**, and **RabbitMQ for message queuing** to efficiently detect and classify playing cards.

It supports **both CPU and GPU configurations** to enable flexible deployment on different hardware.

---

## **Features**
- 🎥 **Processes RTSP video streams**
- 🃏 **Detects and classifies playing cards using YOLO**
- 🏃 **Tracks detected objects with DeepSORT**
- 📨 **Publishes detection results via RabbitMQ**
- 🗄 **Stores stream data using SQLite**
- 🖥 **Runs on CPU or GPU with Docker support**
- ⚙️ **Configurable confidence thresholds and tracking parameters**

---

## **System Architecture**
The project follows a microservices-based architecture, with the following components:

1. **YOLO Inference Service**  
   - Loads YOLO model for inference
   - Processes frames and detects playing cards
   - Publishes detection results to RabbitMQ

2. **DeepSORT Tracker**  
   - Assigns unique IDs to detected objects
   - Tracks objects across multiple frames
   - Associates detections with previous tracks

3. **RabbitMQ**  
   - Acts as a message broker for detection results
   - Enables decoupled communication between services

4. **SQLite Database**  
   - Stores stream configurations
   - Tracks which streams are currently being processed

5. **Web UI (Optional)**  
   - Provides a front-end interface to visualize results

---

## **Installation**

### **1. Prerequisites**
Ensure that your system has the following installed:

- 🐍 Python 3.x
- 🐋 Docker & Docker Compose
- 📦 pip (Python package manager)
- 🖥 NVIDIA GPU & CUDA (if using GPU version)

### **2. Clone the Repository**
```sh
git clone https://github.com/DavidVardzelian/Card_Detection_System.git
cd Card_Detection_System
```

### **3. Set Up Environment**
Modify the `config/settings.yaml` file to customize parameters such as:
- **RabbitMQ host/user/password**
- **Model confidence threshold**
- **YOLO model path**
- **RTSP stream sources**

### **4. Build and Start the Services**
For **CPU Mode**:
```sh
bash scripts/run_local.sh cpu
```

For **GPU Mode**:
```sh
bash scripts/run_local.sh gpu
```

---

## **Configuration**
The **`config/settings.yaml`** file defines runtime parameters:

```yaml
rabbitmq_host: "rabbitmq"
rabbitmq_user: "admin"
rabbitmq_pass: "admin"
rabbitmq_queue_yolo: "yolo-detections"

confidence_threshold: 0.94
model_path: "models/best.pt"

retry_delay: 30
```

Modify the values based on your system and model requirements.

---

## **Usage**
Once the system is running:

### **Viewing Logs**
To monitor service logs, run:
```sh
docker-compose -f docker-compose_CPUv.yml logs -f
```
Or for GPU mode:
```sh
docker-compose -f docker-compose_GPUv.yml logs -f
```

### **RabbitMQ Management UI**
Access RabbitMQ via browser:
```
http://localhost:15672
```
(Default credentials: `admin` / `admin`)

### **Viewing Published Detections**
The detected card information is published to RabbitMQ queues named **yolo-detections_TABLEID**. You can subscribe to the queue and consume messages in JSON format.

---

## **Project Structure**
```
rtsp-card-detection/
│── docker/                         # Docker configuration
│   ├── yolo_inference.Dockerfile   # Dockerfile for YOLO inference service
│   ├── web_ui.Dockerfile           # Dockerfile for web UI
│   ├── db.Dockerfile                # Dockerfile for database service
│
│── models/                          # YOLO model files
│── src/                              # Source code
│   ├── yolo_inference.py            # Main YOLO inference script
│   ├── deep_sort_tracker.py         # DeepSORT tracker
│   ├── card_mapper.py               # Card class ID to name mapping
│
│── scripts/
│   ├── run_local.sh                 # Script to start services
│
│── config/
│   ├── settings.yaml                 # Configuration file
│
│── docker-compose.yml                 # Main Docker Compose file
│── docker-compose_CPUv.yml            # CPU version of Docker Compose
│── docker-compose_GPUv.yml            # GPU version of Docker Compose
│── README.md                          # Project documentation
```

---

## **Future Enhancements**
- ✅ Add **support for multiple RTSP streams**
- ✅ Implement **real-time visualization of detected objects**
- ✅ Optimize **YOLO model inference speed**
- ✅ Improve **DeepSORT tracking accuracy**

---

## **Contributors**
👨‍💻 **David Vardzelian** – 
📧 Contact: [your.email@example.com](mailto:david.vardzelian@gmail.com)  

