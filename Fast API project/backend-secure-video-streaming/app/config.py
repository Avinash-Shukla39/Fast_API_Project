import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/video_db")
    KAFKA_SERVERS = os.getenv("KAFKA_SERVERS", "localhost:9092")
    ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY", "your-encryption-key-here")
    VIDEO_UPLOAD_TOPIC = "video_uploads"
    VIDEO_STREAM_TOPIC = "video_streams"