import React from 'react';
import { useParams } from 'react-router-dom';
import VideoPlayer from '../../components/VideoPlayer';
import './Stream.css';

const Stream = () => {
  const { videoId } = useParams();

  return (
    <div className="stream-page">
      <h1>Video Streaming</h1>
      <VideoPlayer videoId={videoId} />
    </div>
  );
};

export default Stream;