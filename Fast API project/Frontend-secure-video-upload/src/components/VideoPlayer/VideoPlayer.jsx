import React, { useState, useEffect, useRef } from 'react';
import { useVideoStream } from '../../hooks/useVideoStream';
import './VideoPlayer.css';

const VideoPlayer = ({ videoId }) => {
  const videoRef = useRef(null);
  const { streamUrl, isLoading, error } = useVideoStream(videoId);

  useEffect(() => {
    if (streamUrl && videoRef.current) {
      videoRef.current.src = streamUrl;
    }
  }, [streamUrl]);

  return (
    <div className="video-player-container">
      <h2>Video Player</h2>
      {isLoading && <p className="loading">Loading video stream...</p>}
      {error && <p className="error">{error}</p>}
      <video 
        ref={videoRef} 
        controls 
        className="video-element"
      />
    </div>
  );
};

export default VideoPlayer;