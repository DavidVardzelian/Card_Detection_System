#!/bin/bash

if [ $# -eq 0 ]; then
  echo "ℹ️  No deployment mode specified. Defaulting to CPU mode."
  mode="cpu"
else
  mode="$1"
fi

case "$mode" in
  cpu)
    COMPOSE_FILE="./docker-compose_CPUv.yml"
    echo "✅ Selected CPU mode."
    ;;
  gpu)
    COMPOSE_FILE="./docker-compose_GPUv.yml"
    echo "✅ Selected GPU mode."
    ;;
  *)
    echo "❌ Invalid mode: $mode. Use 'cpu' or 'gpu'."
    exit 1
    ;;
esac

echo "🚀 Starting RTSP Card Detection System Locally using $mode configuration..."

cd "$(dirname "$0")/.."

echo "🔧 Building Docker images..."
docker-compose -f "${COMPOSE_FILE}" up --build -d

echo "✅ All services are up and running!"
echo "🔍 To view logs, use: docker-compose -f ${COMPOSE_FILE} logs -f"
