# Use a lightweight Python image
FROM python:3.9-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*
    
WORKDIR /app

COPY src/rtsp_processor.py /app/
COPY config/settings.yaml /app/config/

RUN pip install opencv-python-headless pika pyyaml numpy

CMD ["python", "rtsp_processor.py"]
