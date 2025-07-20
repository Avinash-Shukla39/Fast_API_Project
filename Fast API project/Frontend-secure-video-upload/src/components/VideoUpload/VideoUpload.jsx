import React, { useState } from 'react';
import { useVideoUpload } from '../../hooks/useVideoUpload';
import './VideoUpload.css';

const VideoUpload = () => {
  const [file, setFile] = useState(null);
  const { uploadProgress, uploadVideo, error } = useVideoUpload();

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) return;
    await uploadVideo(file);
  };

  return (
    <div className="video-upload-container">
      <h2>Upload Video</h2>
      <div className="upload-form">
        <input 
          type="file" 
          accept="video/*" 
          onChange={handleFileChange} 
          className="file-input"
        />
        <button 
          onClick={handleUpload} 
          disabled={!file || uploadProgress > 0}
          className="upload-button"
        >
          {uploadProgress > 0 ? 'Uploading...' : 'Upload'}
        </button>
        {uploadProgress > 0 && (
          <div className="progress-container">
            <progress 
              value={uploadProgress} 
              max="100" 
              className="progress-bar"
            />
            <span>{uploadProgress}%</span>
          </div>
        )}
        {error && <p className="error-message">{error}</p>}
      </div>
    </div>
  );
};

export default VideoUpload;