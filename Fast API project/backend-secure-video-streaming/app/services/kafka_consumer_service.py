from app.config import Config
from app.services.video_service import VideoService
from kafka import KafkaConsumer
import json
import threading

class KafkaConsumerService:
    def __init__(self):
        self.consumer = KafkaConsumer(
            Config.VIDEO_UPLOAD_TOPIC,
            bootstrap_servers=Config.KAFKA_SERVERS,
            group_id='video-processing-group',
            auto_offset_reset='earliest',
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        self.video_service = VideoService()

    def start_consuming(self):
        def consume():
            for message in self.consumer:
                try:
                    data = message.value
                    print(f"Processing video: {data['video_id']}")
                    # Add any additional processing logic here
                except Exception as e:
                    print(f"Error processing message: {e}")

        thread = threading.Thread(target=consume, daemon=True)
        thread.start()