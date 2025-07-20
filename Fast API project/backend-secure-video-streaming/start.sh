#!/bin/bash
#!/bin/bash

# Start Kafka consumer in background
python -m app.services.kafka_consumer_service &

# Start the FastAPI application
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload