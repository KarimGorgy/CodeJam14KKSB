import React, { useState } from "react";
import IntroPage from "./pages/IntroPage";
import ChatPage from "./pages/ChatPage";

const App = () => {
  const [showIntro, setShowIntro] = useState(true);

  const handleStart = () => {
    setShowIntro(false); // Transition to ChatPage
  };

  return showIntro ? <IntroPage onStart={handleStart} /> : <ChatPage />;
};

export default App;
