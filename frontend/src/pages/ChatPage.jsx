import React, { useState, useEffect, useRef } from "react";
import ChatBubble from "../components/ChatBubble";
import Sidebar from "../components/Sidebar";
import InputBar from "../components/InputBar";
import VehicleSlider from "../components/VehicleSlider";
import "../styles/ChatPage.css";
import logo from "../assets/matador-logo.png";
import eclogo from "../assets/esto-car-4-you.png";
import { v4 as uuidv4 } from 'uuid';

const ChatPage = () => {
  const [selectedVehicles, setSelectedVehicles] = useState([]); // State for selected vehicles
  
  const [conversations, setConversations] = useState([
    { id: 1, name: "Conversation 1", messages: [] },
  ]);
  const [currentConversation, setCurrentConversation] = useState(1);
  const [nextConversationId, setNextConversationId] = useState(2);
  const [vehicleResults, setVehicleResults] = useState([]);
  const handleCompareClick = () => {
    if (selectedVehicles.length > 0) {
      navigate("/comparison", { state: { vehicles: selectedVehicles } }); // Pass vehicles via state
    } else {
      alert("Please select at least one vehicle to compare.");
    }
  };
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
  const [sessionId] = useState(() => uuidv4());

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
      const response = await fetch("http://127.0.0.1:5000/message", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ userMessage, sessionId }),
      });

      if (response.ok) {
      const data = await response.json();
      console.log("Response from backend:", data); // Debug log

      const botResponse = data.response || "Sorry, I didn't understand that.";
      const recommendations = data.fulfillmentMessages || [];

      // Add bot's response to the conversation
      setConversations((prev) =>
        prev.map((conversation) =>
          conversation.id === currentConversation
            ? {
                ...conversation,
                messages: [...conversation.messages, { sender: "bot", text: botResponse }],
              }
            : conversation
        )
      );

      // Update vehicle results if recommendations are available
      if (recommendations.length > 0) {
        setVehicleResults(recommendations);
      } else {
        setVehicleResults([]);
      }
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
            <img src={eclogo} alt="EC4U Logo" />
            <h1>EC4U Chatbot</h1>
          </div>
        </div>

        <div className="chat-area" ref={chatAreaRef}>
          {currentMessages.map((msg, index) => (
            <ChatBubble key={index} sender={msg.sender} text={msg.text} />
          ))}
        </div>

         {/* Only enable navigation if vehicles are available */}
         {vehicleResults.length > 0 && (
          <>
            <button
                onClick={handleCompareClick} // Pass the vehicles for comparison
                className="compare-btn"
            
            >
              Compare Vehicles
            </button>
            <VehicleSlider
              vehicles={vehicleResults}
              onSelect={(vehicle) => {
                if (!selectedVehicles.includes(vehicle) && selectedVehicles.length < 3) {
                  setSelectedVehicles((prev) => [...prev, vehicle]);
                }
              }}
            />
          </>
        )}

        <InputBar onSend={handleSend} />
      </div>
    </div>
  );
};

export default ChatPage;