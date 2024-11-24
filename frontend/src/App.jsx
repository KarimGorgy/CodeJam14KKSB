import React, { useState } from "react";
import IntroPage from "./pages/IntroPage";
import ChatPage from "./pages/ChatPage";
import ComparisonPage from "./pages/ComparisonPage";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { VehicleProvider } from "./context/VehicleContext"; // Correct Import

const App = () => {
  const [showIntro, setShowIntro] = useState(true); // Track intro visibility

  const handleStart = () => {
    setShowIntro(false); // Transition to ChatPage
  };

  return (
    <VehicleProvider> 
      <Router>
        <Routes>
          <Route
            path="/"
            element={showIntro ? <IntroPage onStart={handleStart} /> : <ChatPage />}
          />
          <Route path="/comparison" element={<ComparisonPage />} />
        </Routes>
      </Router>
    </VehicleProvider>
  );
};

export default App;
