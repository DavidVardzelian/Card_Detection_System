# Use CPU-only base image (Remove CUDA)
FROM python:3.8-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip\
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy application files
COPY src/yolo_inference.py /app/
COPY src/card_mapper.py . 
COPY config/ /app/config/
COPY models /app/models

# Install dependencies
RUN pip install ultralytics deep_sort_realtime pika pyyaml numpy

# Start the YOLO Inference Module
CMD ["python", "yolo_inference.py"]
