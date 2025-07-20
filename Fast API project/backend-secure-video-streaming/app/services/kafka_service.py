from kafka import KafkaProducer, KafkaConsumer
from kafka.admin import KafkaAdminClient, NewTopic
import json
import asyncio
from typing import AsyncGenerator
from app.config import Config

class KafkaProducerService:
    def __init__(self):
        self.producer = KafkaProducer(
            bootstrap_servers=Config.KAFKA_SERVERS,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            acks='all',
            retries=3
        )
    
    def send_message(self, topic: str, message: dict):
        try:
            future = self.producer.send(topic, message)
            future.add_errback(self._handle_kafka_error)
        except Exception as e:
            print(f"Failed to send message to Kafka: {e}")
            raise

    def _handle_kafka_error(self, exc):
        print(f"Kafka producer error: {exc}")
        # Add retry logic here if needed

class KafkaConsumerService:
    def __init__(self, topic: str, group_id: str):
        self.consumer = KafkaConsumer(
            topic,
            bootstrap_servers=Config.KAFKA_SERVERS,
            group_id=group_id,
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            value_deserializer=lambda x: json.loads(x.decode('utf-8')),
            consumer_timeout_ms=10000
        )
        self._running = False

    async def consume_messages(self) -> AsyncGenerator[dict, None]:
        """Asynchronously consume messages from Kafka"""
        self._running = True
        try:
            while self._running:
                for message in self.consumer:
                    yield message.value
                    if not self._running:
                        break
        finally:
            self.close()

    def close(self):
        self._running = False
        self.consumer.close()

class KafkaAdminService:
    @staticmethod
    def create_topic(topic_name: str):
        admin_client = KafkaAdminClient(
            bootstrap_servers=Config.KAFKA_SERVERS
        )
        
        topic_list = [NewTopic(
            name=topic_name,
            num_partitions=1,
            replication_factor=1
        )]
        
        try:
            admin_client.create_topics(new_topics=topic_list, validate_only=False)
            print(f"Topic {topic_name} created successfully")
        except Exception as e:
            print(f"Failed to create topic {topic_name}: {e}")
        finally:
            admin_client.close()