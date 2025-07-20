import React from 'react';
import VideoUpload from '../../components/VideoUpload';
import './Upload.css';

const Upload = () => {
  return (
    <div className="upload-page">
      <h1>Upload Your Video</h1>
      <VideoUpload />
    </div>
  );
};

export default Upload;