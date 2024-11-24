import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './styles/global.css'; // Import global styles
import { VehicleProvider } from './context/VehicleContext'; // Corrected import

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <VehicleProvider>
      <App />
    </VehicleProvider>
  </React.StrictMode>
);
