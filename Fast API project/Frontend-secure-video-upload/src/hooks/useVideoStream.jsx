import { useState, useEffect } from 'react';
import { streamVideo } from '../services/videoService';

export const useVideoStream = (videoId) => {
  const [streamUrl, setStreamUrl] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchStream = async () => {
      if (!videoId) return;

      setIsLoading(true);
      setError(null);

      try {
        const blob = await streamVideo(videoId);
        const url = URL.createObjectURL(blob);
        setStreamUrl(url);
      } catch (err) {
        setError(err);
      } finally {
        setIsLoading(false);
      }
    };

    fetchStream();

    return () => {
      if (streamUrl) {
        URL.revokeObjectURL(streamUrl);
      }
    };
  }, [videoId]);

  return { streamUrl, isLoading, error };
};