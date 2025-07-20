import api from './api';

export const uploadVideo = async (file, onUploadProgress) => {
  const formData = new FormData();
  formData.append('video', file);

  try {
    const response = await api.post('/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      onUploadProgress,
    });
    return response.data;
  } catch (error) {
    throw error.response?.data?.message || 'Upload failed';
  }
};

export const streamVideo = async (videoId) => {
  try {
    const response = await api.get(`/stream/${videoId}`, {
      responseType: 'blob',
    });
    return response.data;
  } catch (error) {
    throw error.response?.data?.message || 'Streaming failed';
  }
};