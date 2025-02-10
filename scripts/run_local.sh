#!/bin/bash

echo "🚀 Starting RTSP Card Detection System Locally..."

cd "$(dirname "$0")/.."

echo "🔧 Building Docker images..."
docker-compose -f ./docker-compose.yml up --build -d
docker-compose 

echo "✅ All services are up and running!"
echo "🔍 To view logs, use: docker-compose logs -f"
