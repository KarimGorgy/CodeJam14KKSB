import React, { useState } from "react";
import "../styles/IntroPage.css";
import logo from "../assets/matador-logo.png";
import eclogo from "../assets/esto-car-4-you.png";

const IntroPage = ({ onStart }) => {
  const [animateButton, setAnimateButton] = useState(false);
  const [fadeOut, setFadeOut] = useState(false);

  const handleClick = () => {
    setAnimateButton(true); // Trigger button animation
    setTimeout(() => {
      setFadeOut(true); // Trigger page fade-out animation
    }, 500); // Delay fade-out slightly after button click
    setTimeout(() => {
      onStart(); // Call the parent function to navigate to ChatPage
    }, 1500); // Match the overall animation duration
  };

  return (
    <div className={`intro-page ${fadeOut ? "fade-out" : ""}`}>
      <div className="intro-header">
        <div className="logo-container-horizontal">
          <img src={logo} alt="Matador Logo" className="logo" />
          <span className="collab-x">X</span>
          <img src={eclogo} alt="EC4U Logo" className="logo" />
        </div>
        <h1>Welcome to Matador's Esto-Car 4 You</h1>
        <p>Your trusted conversational AI for automotive dealerships.</p>
      </div>
      <button
        className={`start-button ${animateButton ? "animate" : ""}`}
        onClick={handleClick}
      >
        Get Started
      </button>
    </div>
  );
};

export default IntroPage;
