FROM python:3.8-slim

WORKDIR /app

COPY src/web_ui.py /app/
COPY templates /app/templates
COPY config/settings.yaml /app/config/

RUN pip install flask

CMD ["python", "web_ui.py"]
