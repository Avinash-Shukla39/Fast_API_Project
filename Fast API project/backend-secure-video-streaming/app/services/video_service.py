import uuid
from fastapi import UploadFile
from typing import Dict, Optional
from app.config import Config
from app.services.encryption import encrypt_data, decrypt_data
from app.database.models import create_video_record, get_video_by_id
from app.services.kafka_service import KafkaProducerService, KafkaConsumerService
import asyncio
from concurrent.futures import ThreadPoolExecutor

class VideoService:
    def __init__(self):
        self.kafka_producer = KafkaProducerService()
        self.executor = ThreadPoolExecutor(max_workers=4)
        self.active_streams: Dict[str, asyncio.Queue] = {}

    async def upload_video(self, video_file: UploadFile) -> str:
        """Handle video upload with encryption and Kafka notification"""
        try:
            video_id = str(uuid.uuid4())
            content = await video_file.read()
            encrypted_content = encrypt_data(content)
            
            create_video_record(
                video_id=video_id,
                filename=video_file.filename,
                encrypted_data=encrypted_content,
                content_type=video_file.content_type
            )
            
            self.kafka_producer.send_message(
                Config.VIDEO_UPLOAD_TOPIC,
                {
                    'video_id': video_id,
                    'filename': video_file.filename,
                    'action': 'upload_complete'
                }
            )
            
            return video_id
        except Exception as e:
            raise e

    async def initiate_kafka_stream(self, video_id: str) -> asyncio.Queue:
        """Initialize Kafka streaming for a video"""
        if video_id in self.active_streams:
            return self.active_streams[video_id]

        queue = asyncio.Queue()
        self.active_streams[video_id] = queue

        # Start background task to process Kafka messages
        asyncio.create_task(self._kafka_stream_consumer(video_id, queue))
        
        return queue

    async def _kafka_stream_consumer(self, video_id: str, queue: asyncio.Queue):
        """Background task to consume Kafka messages for a video stream"""
        consumer = KafkaConsumerService(
            topic=f"video_stream_{video_id}",
            group_id=f"video_stream_{video_id}_consumer"
        )

        try:
            async for message in consumer.consume_messages():
                await queue.put(message)
                
                if message.get('is_last_chunk', False):
                    break
        finally:
            consumer.close()
            self.active_streams.pop(video_id, None)

    async def stream_video_kafka(self, video_id: str) -> Optional[Dict]:
        """Stream video through Kafka in chunks"""
        try:
            # Get encrypted video from database
            video_record = await asyncio.get_event_loop().run_in_executor(
                self.executor,
                get_video_by_id,
                video_id
            )
            
            if not video_record:
                return None

            encrypted_data, content_type = video_record
            decrypted_data = decrypt_data(encrypted_data)

            # Break into chunks and send to Kafka
            chunk_size = 1024 * 1024  # 1MB chunks
            total_chunks = (len(decrypted_data) // chunk_size + 1
            stream_topic = f"video_stream_{video_id}"

            for i in range(0, len(decrypted_data), chunk_size):
                chunk = decrypted_data[i:i + chunk_size]
                is_last = (i + chunk_size) >= len(decrypted_data)

                self.kafka_producer.send_message(
                    stream_topic,
                    {
                        'video_id': video_id,
                        'chunk_index': i // chunk_size,
                        'total_chunks': total_chunks,
                        'data': chunk.decode('latin-1'),
                        'content_type': content_type,
                        'is_last_chunk': is_last
                    }
                )

            return {
                'video_id': video_id,
                'stream_topic': stream_topic,
                'total_chunks': total_chunks,
                'content_type': content_type
            }
        except Exception as e:
            raise e

    async def get_video_metadata(self, video_id: str) -> Optional[Dict]:
        """Get video metadata without streaming"""
        try:
            video_data = await asyncio.get_event_loop().run_in_executor(
                self.executor,
                get_video_by_id,
                video_id
            )
            
            if not video_data:
                return None

            _, content_type = video_data
            return {
                'video_id': video_id,
                'content_type': content_type
            }
        except Exception as e:
            raise e