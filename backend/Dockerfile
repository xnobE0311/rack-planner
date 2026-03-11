FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY backend/ /app/backend/
COPY data/ /app/data/

RUN python -m pip install --upgrade pip \
    && pip install --no-cache-dir -e /app/backend

EXPOSE 8000

ENV RACK_PLANNER_ALLOWED_ORIGINS="http://localhost:5173,http://127.0.0.1:5173" \
    RACK_PLANNER_CORS_ALLOW_CREDENTIALS="false" \
    RACK_PLANNER_DEVICES_PATH="/app/data/devices/default_devices.json"

CMD ["uvicorn", "rack_planner.app:app", "--host", "0.0.0.0", "--port", "8000"]
