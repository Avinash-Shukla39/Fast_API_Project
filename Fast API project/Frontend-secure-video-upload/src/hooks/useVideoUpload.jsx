import { useState } from 'react';
import { uploadVideo } from '../services/videoService';

export const useVideoUpload = () => {
  const [uploadProgress, setUploadProgress] = useState(0);
  const [error, setError] = useState(null);

  const uploadVideo = async (file) => {
    setError(null);
    setUploadProgress(0);

    try {
      const onUploadProgress = (progressEvent) => {
        const progress = Math.round(
          (progressEvent.loaded * 100) / progressEvent.total
        );
        setUploadProgress(progress);
      };

      const response = await uploadVideo(file, onUploadProgress);
      return response;
    } catch (err) {
      setError(err);
      throw err;
    } finally {
      if (uploadProgress === 100) {
        setTimeout(() => setUploadProgress(0), 2000);
      }
    }
  };

  return { uploadProgress, uploadVideo, error };
};