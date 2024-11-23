import React, { useState } from "react";
import "../styles/InputBar.css";

const InputBar = ({ onSend }) => {
  const [input, setInput] = useState("");

  const handleSend = () => {
    if (input.trim()) {
      onSend(input); // Send the message
      setInput("");  // Clear the input field
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter") {
      handleSend(); // Trigger send on Enter key
    }
  };

  return (
    <div className="footer">
      <input
        type="text"
        placeholder="Type your message..."
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyPress={handleKeyPress} // Listen for key presses
      />
      <button onClick={handleSend}>Send</button>
    </div>
  );
};

export default InputBar;
