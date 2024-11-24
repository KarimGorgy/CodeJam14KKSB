import React, { useEffect, useState, useContext } from "react";
import "../styles/ComparisonPage.css";
import { VehicleContext } from "../context/VehicleContext"; // Import VehicleContext

const ComparisonPage = () => {
  const { vehicles, selectedVehicles, setSelectedVehicles } = useContext(VehicleContext); // Use context
  const [vehicleDetails, setVehicleDetails] = useState([]); // Store details fetched from backend

  const handleSelectVehicle = (event) => {
    const selectedId = event.target.value;
    const selectedVehicle = vehicles.find((vehicle) => vehicle.VIN === selectedId);

    if (
      selectedVehicle &&
      selectedVehicles.length < 2 &&
      !selectedVehicles.some((v) => v.VIN === selectedId)
    ) {
      setSelectedVehicles((prev) => {
        const updatedVehicles = [...prev, selectedVehicle];
        console.log("Updated selectedVehicles:", updatedVehicles); // Debug log
        return updatedVehicles;
      });
    } else {
      console.warn("Vehicle already selected or limit reached.");
    }
  };

  const handleRemoveVehicle = (vin) => {
    setSelectedVehicles((prev) => prev.filter((vehicle) => vehicle.VIN !== vin)); // Remove vehicle
    setVehicleDetails((prev) => prev.filter((detail) => detail.VIN !== vin)); // Remove details
  };

  useEffect(() => {
    console.log("useEffect triggered. Selected Vehicles:", selectedVehicles);

    const fetchDetails = async () => {
      if (selectedVehicles.length > 0) {
        const vinList = selectedVehicles.map((vehicle) => vehicle.VIN);
        console.log("Fetching details for VINs:", vinList);

        try {
          const response = await fetch("http://127.0.0.1:5000/compare", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ vinList }),
          });

          if (response.ok) {
            const details = await response.json();
            console.log("Comparison data received:", details);
            setVehicleDetails(details);
          } else {
            console.error("Error fetching comparison data:", response.statusText);
          }
        } catch (error) {
          console.error("Error connecting to backend:", error);
        }
      }
    };

    fetchDetails();
  }, [selectedVehicles]); // Triggered when `selectedVehicles` changes

  return (
    <div className="comparison-page">
      <h1>Compare Vehicles</h1>
      <div className="vehicle-selector">
        <label htmlFor="vehicle-select">Select a Vehicle to Compare:</label>
        <select id="vehicle-select" onChange={handleSelectVehicle}>
          <option value="">-- Select a Vehicle --</option>
          {Array.isArray(vehicles) && vehicles.length > 0 ? (
            vehicles.map((vehicle) => (
              <option key={vehicle.VIN} value={vehicle.VIN}>
                {`${vehicle.Year} ${vehicle.Make} ${vehicle.Model}`}
              </option>
            ))
          ) : (
            <option disabled>No vehicles available</option>
          )}
        </select>
      </div>

      {selectedVehicles.length > 0 ? (
        <div className="comparison-section">
          <div className="comparison-grid">
            {selectedVehicles.map((vehicle, index) => (
              <div key={vehicle.VIN} className="vehicle-card">
                <h2>{`${vehicle.Year} ${vehicle.Make} ${vehicle.Model}`}</h2>
                <p><strong>Price:</strong> ${vehicle.SellingPrice}</p>
                <p><strong>Miles:</strong> {vehicle.Miles} miles</p>
                <p><strong>Color:</strong> {vehicle.Ext_Color_Generic}</p>
                <p><strong>Drivetrain:</strong> {vehicle.Drivetrain}</p>
                <button
                  className="remove-btn"
                  onClick={() => handleRemoveVehicle(vehicle.VIN)}
                >
                  Remove
                </button>
              </div>
            ))}
          </div>
        </div>
      ) : (
        <p>No vehicles selected for comparison.</p>
      )}

      {selectedVehicles.length === 2 && vehicleDetails.length === 2 && (
        <div className="comparison-table">
          <h2>Side-by-Side Comparison</h2>
          <table>
            <thead>
              <tr>
                <th>Feature</th>
                <th>{`${selectedVehicles[0].Year} ${selectedVehicles[0].Make} ${selectedVehicles[0].Model}`}</th>
                <th>{`${selectedVehicles[1].Year} ${selectedVehicles[1].Make} ${selectedVehicles[1].Model}`}</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>Price</td>
                <td>${vehicleDetails[0].SellingPrice}</td>
                <td>${vehicleDetails[1].SellingPrice}</td>
              </tr>
              <tr>
                <td>Miles</td>
                <td>{vehicleDetails[0].Miles} miles</td>
                <td>{vehicleDetails[1].Miles} miles</td>
              </tr>
              <tr>
                <td>Color</td>
                <td>{vehicleDetails[0].Ext_Color_Generic}</td>
                <td>{vehicleDetails[1].Ext_Color_Generic}</td>
              </tr>
              <tr>
                <td>Drivetrain</td>
                <td>{vehicleDetails[0].Drivetrain}</td>
                <td>{vehicleDetails[1].Drivetrain}</td>
              </tr>
              <tr>
                <td>Fuel Type</td>
                <td>{vehicleDetails[0].Fuel_Type}</td>
                <td>{vehicleDetails[1].Fuel_Type}</td>
              </tr>
              <tr>
                <td>City MPG</td>
                <td>{vehicleDetails[0].CityMPG}</td>
                <td>{vehicleDetails[1].CityMPG}</td>
              </tr>
              <tr>
                <td>Highway MPG</td>
                <td>{vehicleDetails[0].HighwayMPG}</td>
                <td>{vehicleDetails[1].HighwayMPG}</td>
              </tr>
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default ComparisonPage;
