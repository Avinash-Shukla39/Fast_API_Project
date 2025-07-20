Setup Instructions:
Create the virtual environment and install dependencies:


python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt



Set up PostgreSQL database:


createdb video_db
psql video_db -f app/database/schema.sql








Start Kafka:


# Start Zookeeper
zookeeper-server-start.sh config/zookeeper.properties

# Start Kafka
kafka-server-start.sh config/server.properties

# Create topics
kafka-topics --create --topic video_uploads --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
kafka-topics --create --topic video_streams --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1













Run the application:
chmod +x start.sh
./start.sh