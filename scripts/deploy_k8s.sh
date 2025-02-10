#!/bin/bash

echo "🚀 Deploying RTSP Card Detection System to Kubernetes..."

cd "$(dirname "$0")/.."

echo "🔧 Applying Kubernetes configurations..."
kubectl apply -f k8s/rabbitmq-deployment.yaml
kubectl apply -f k8s/rtsp-processor-deployment.yaml
kubectl apply -f k8s/yolo-inference-deployment.yaml

echo "⏳ Waiting for services to start..."
kubectl wait --for=condition=ready pod --all --timeout=180s

echo "✅ Services running in Kubernetes:"
kubectl get services

echo "📌 To check logs: kubectl logs -f <pod-name>"
