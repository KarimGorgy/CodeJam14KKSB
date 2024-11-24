// InputBar.jsx
import React, { useState } from "react";
import "../styles/InputBar.css";

const InputBar = ({ onSend }) => {
  const [input, setInput] = useState("");

  const handleSend = (e) => {
    e.preventDefault(); // Prevent form submission default behavior
    if (input.trim()) {
      onSend(input); // Pass user's message to parent
      setInput(""); // Clear the input field
    }
  };

  return (
    <div className="footer">
      <form onSubmit={handleSend}>
        <input
          type="text"
          placeholder="Type your message..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          // Removed onKeyDown handler
        />
        <button type="submit">Send</button>
      </form>
    </div>
  );
};

export default InputBar;
