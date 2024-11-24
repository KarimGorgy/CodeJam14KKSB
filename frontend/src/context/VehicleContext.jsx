import React, { createContext, useState } from "react";

// Create the VehicleContext
export const VehicleContext = createContext();

// Create a provider component
export const VehicleProvider = ({ children }) => {
  const [vehicles, setVehicles] = useState([]); // Global state for vehicles
  const [selectedVehicles, setSelectedVehicles] = useState([]); // Selected vehicles for comparison

  return (
    <VehicleContext.Provider
      value={{
        vehicles,
        setVehicles,
        selectedVehicles,
        setSelectedVehicles,
      }}
    >
      {children}
    </VehicleContext.Provider>
  );
};
