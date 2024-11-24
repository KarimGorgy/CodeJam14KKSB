// ChatPage.jsx
import React, { useState, useEffect, useRef } from "react";
import ChatBubble from "../components/ChatBubble";
import Sidebar from "../components/Sidebar";
import InputBar from "../components/InputBar";
import VehicleSlider from "../components/VehicleSlider";
import "../styles/ChatPage.css";
import logo from "../assets/matador-logo.png";

const ChatPage = () => {
  const [conversations, setConversations] = useState([
    { id: 1, name: "Conversation 1", messages: [] },
  ]);
  const [currentConversation, setCurrentConversation] = useState(1);
  const [nextConversationId, setNextConversationId] = useState(2);
  const [vehicleResults, setVehicleResults] = useState([]);

  const chatAreaRef = useRef(null);

  const addConversation = () => {
    const newConversationId = nextConversationId;
    setConversations((prev) => [
      ...prev,
      { id: newConversationId, name: `Conversation ${newConversationId}`, messages: [] },
    ]);
    setCurrentConversation(newConversationId);
    setNextConversationId((prev) => prev + 1);
  };

  const deleteConversation = (id) => {
    const updatedConversations = conversations.filter((conv) => conv.id !== id);
    if (updatedConversations.length > 0) {
      setConversations(updatedConversations);
      setCurrentConversation(updatedConversations[0].id);
    } else {
      setConversations([]);
      setCurrentConversation(null);
    }
  };

  const handleSend = async (userMessage) => {
    if (!currentConversation) return;

    // Add user's message to the conversation
    setConversations((prev) =>
      prev.map((conversation) =>
        conversation.id === currentConversation
          ? {
              ...conversation,
              messages: [...conversation.messages, { sender: "user", text: userMessage }],
            }
          : conversation
      )
    );

    try {
      console.log("Sending request to backend:", userMessage); // Debug log
      const response = await fetch("http://127.0.0.1:5000/filter", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ userMessage }),
      });

      if (response.ok) {
        const vehicles = await response.json();
        console.log("Response from backend:", vehicles); // Debug log
        setVehicleResults(vehicles);
        // Add bot's response to the conversation
        setConversations((prev) =>
          prev.map((conversation) =>
            conversation.id === currentConversation
              ? {
                  ...conversation,
                  messages: [
                    ...conversation.messages,
                    { sender: "bot", text: "Here are some options!" },
                  ],
                }
              : conversation
          )
        );
      } else {
        // Handle error response
        setConversations((prev) =>
          prev.map((conversation) =>
            conversation.id === currentConversation
              ? {
                  ...conversation,
                  messages: [
                    ...conversation.messages,
                    { sender: "bot", text: "Sorry, something went wrong!" },
                  ],
                }
              : conversation
          )
        );
      }
    } catch (error) {
      console.error("Error communicating with backend:", error); // Log error
      setConversations((prev) =>
        prev.map((conversation) =>
          conversation.id === currentConversation
            ? {
                ...conversation,
                messages: [
                  ...conversation.messages,
                  { sender: "bot", text: "Error connecting to backend!" },
                ],
              }
            : conversation
        )
      );
    }
  };

  useEffect(() => {
    if (chatAreaRef.current) {
      chatAreaRef.current.scrollTop = chatAreaRef.current.scrollHeight;
    }
  }, [conversations, currentConversation]);

  const currentMessages =
    conversations.find((conv) => conv.id === currentConversation)?.messages || [];

  return (
    <div className="chat-page">
      <Sidebar
        conversations={conversations}
        onAdd={addConversation}
        onDelete={deleteConversation}
        onSelect={(id) => setCurrentConversation(id)}
        activeConversation={currentConversation}
      />

      <div className="chat-container">
        <div className="header">
          <div className="logo">
            <img src={logo} alt="Matador Logo" />
            <h1>Matador Chatbot</h1>
          </div>
        </div>

        <div className="chat-area" ref={chatAreaRef}>
          {currentMessages.map((msg, index) => (
            <ChatBubble key={index} sender={msg.sender} text={msg.text} />
          ))}
        </div>

        {vehicleResults.length > 0 && <VehicleSlider vehicles={vehicleResults} />}

        <InputBar onSend={handleSend} />
      </div>
    </div>
  );
};

export default ChatPage;
