
from fastapi import FastAPI

app = FastAPI(
    title="Secure Video Streaming API",
    description="API for secure video upload and streaming with encryption",
    version="1.0.0"
)

# Import routes
from app.routes import video_routes