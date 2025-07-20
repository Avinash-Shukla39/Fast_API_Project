import React from 'react';
import './Footer.css';

const Footer = () => {
  return (
    <footer className="footer">
      <p>© {new Date().getFullYear()} Secure Video Streaming. All rights reserved.</p>
    </footer>
  );
};

export default Footer;