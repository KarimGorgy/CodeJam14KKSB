import React, { useState } from "react";
import "../styles/IntroPage.css";
import logo from "../assets/matador-logo.png";

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
        <img src={logo} alt="Matador Logo" className="logo" />
        <h1>Welcome to Matador AI</h1>
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
