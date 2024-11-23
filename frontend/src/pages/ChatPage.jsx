import React, { useState, useEffect, useRef } from "react";
import ChatBubble from "../components/ChatBubble";
import Sidebar from "../components/Sidebar";
import "../styles/ChatPage.css";
import logo from "../assets/matador-logo.png";

const ChatPage = () => {
  const [conversations, setConversations] = useState([
    { id: 1, name: "Conversation 1", messages: [] },
  ]); // Stores all conversations
  const [currentConversation, setCurrentConversation] = useState(1); // Tracks the active conversation
  const [inputValue, setInputValue] = useState(""); // State for input value
  const [nextConversationId, setNextConversationId] = useState(2); // Tracks the next conversation ID

  const chatAreaRef = useRef(null); // Reference to the chat area

  // Add a new conversation
  const addConversation = () => {
    const newConversationId = nextConversationId;
    setConversations((prev) => [
      ...prev,
      { id: newConversationId, name: `Conversation ${newConversationId}`, messages: [] },
    ]);
    setCurrentConversation(newConversationId); // Switch to the new conversation
    setNextConversationId((prev) => prev + 1); // Increment the next conversation ID
  };

  // Delete a conversation
  const deleteConversation = (id) => {
    const updatedConversations = conversations.filter((conv) => conv.id !== id);
    if (updatedConversations.length > 0) {
      setConversations(updatedConversations);
      setCurrentConversation(updatedConversations[0].id); // Set the current conversation to the first available one
    } else {
      setConversations([]);
      setCurrentConversation(null); // No active conversation
    }
  };

  // Handle sending messages
  const handleSend = () => {
    if (inputValue.trim() === "" || !currentConversation) return; // Prevent empty messages
    const updatedConversations = conversations.map((conversation) =>
      conversation.id === currentConversation
        ? {
            ...conversation,
            messages: [
              ...conversation.messages,
              { sender: "user", text: inputValue },
              { sender: "bot", text: "Let me look that up for you!" },
            ],
          }
        : conversation
    );
    setConversations(updatedConversations);
    setInputValue(""); // Clear input field
  };

  // Scroll to the bottom of chat-area whenever messages are added
  useEffect(() => {
    if (chatAreaRef.current) {
      chatAreaRef.current.scrollTop = chatAreaRef.current.scrollHeight;
    }
  }, [conversations, currentConversation]);

  // Get messages of the current conversation
  const currentMessages =
    conversations.find((conv) => conv.id === currentConversation)?.messages || [];

  return (
    <div className="chat-page">
      {/* Sidebar */}
      <Sidebar
        conversations={conversations}
        onAdd={addConversation}
        onDelete={deleteConversation}
        onSelect={(id) => setCurrentConversation(id)}
        activeConversation={currentConversation}
      />

      {/* Main Chat Area */}
      <div className="chat-container">
        <div className="header">
          <div className="logo">
            <img src={logo} alt="Matador Logo" />
            <h1>Matador Chatbot</h1>
          </div>
        </div>

        {/* Chat Messages */}
        <div className="chat-area" ref={chatAreaRef}>
          {currentMessages.map((msg, index) => (
            <ChatBubble key={index} sender={msg.sender} text={msg.text} />
          ))}
        </div>

        {/* Footer with Input */}
        <div className="footer">
          <input
            type="text"
            value={inputValue}
            placeholder="Type your message..."
            onChange={(e) => setInputValue(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") handleSend(); // Send on Enter key
            }}
          />
          <button onClick={handleSend}>Send</button>
        </div>
      </div>
    </div>
  );
};

export default ChatPage;
