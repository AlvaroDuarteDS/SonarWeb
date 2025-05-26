#!/bin/bash
echo "Starting microservices..."

# Start each service in background
uvicorn api.audio_api:app --host 0.0.0.0 --port 8001 &
uvicorn api.browser_api:app --host 0.0.0.0 --port 8002 &
uvicorn api.vision_api:app --host 0.0.0.0 --port 8003 &
uvicorn api.gateway:app --host 0.0.0.0 --port 8000 &

echo "All services started!"
echo "API Gateway: http://localhost:8000"