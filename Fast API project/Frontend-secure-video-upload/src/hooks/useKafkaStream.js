// New hook: useKafkaStream.js
import { useEffect, useState } from 'react';
import { Kafka } from 'kafkajs';

export const useKafkaStream = (videoId) => {
  const [streamUrl, setStreamUrl] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const kafka = new Kafka({
      brokers: [process.env.REACT_APP_KAFKA_BROKER],
    });

    const consumer = kafka.consumer({ groupId: 'video-player-group' });
    
    const run = async () => {
      await consumer.connect();
      await consumer.subscribe({ topic: `video-stream-${videoId}` });
      
      const chunks = {};
      
      await consumer.run({
        eachMessage: async ({ message }) => {
          const data = JSON.parse(message.value);
          chunks[data.chunk_index] = data.data;
          
          if (Object.keys(chunks).length === data.total_chunks) {
            // All chunks received
            const fullData = Object.keys(chunks)
              .sort()
              .map(k => chunks[k])
              .join('');
            
            const byteArray = new Uint8Array(
              [...fullData].map(c => c.charCodeAt(0))
            );
            
            const blob = new Blob([byteArray], { type: 'video/mp4' });
            setStreamUrl(URL.createObjectURL(blob));
          }
        },
      });
    };

    run();
    
    return () => {
      consumer.disconnect();
      if (streamUrl) URL.revokeObjectURL(streamUrl);
    };
  }, [videoId]);

  return { streamUrl, loading };
};