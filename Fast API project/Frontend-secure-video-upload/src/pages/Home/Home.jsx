import React from 'react';
import { Link } from 'react-router-dom';
import './Home.css';

const Home = () => {
  return (
    <div className="home-page">
      <h1>Secure Video Streaming Platform</h1>
      <p>Upload and stream your videos with end-to-end encryption</p>
      <div className="action-buttons">
        <Link to="/upload" className="btn-primary">Upload Video</Link>
      </div>
    </div>
  );
};

export default Home;