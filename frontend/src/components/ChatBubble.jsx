import React from "react";
import "../styles/ChatBubble.css";

const ChatBubble = ({ sender, text }) => {
  return (
    <div className={`chat-bubble ${sender}`}>
      {text}
    </div>
  );
};

export default ChatBubble;
