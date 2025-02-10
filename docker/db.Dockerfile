FROM python:3.8-slim

WORKDIR /app

COPY src/config.py /app/
COPY config /app/config

CMD ["python", "config.py"]
