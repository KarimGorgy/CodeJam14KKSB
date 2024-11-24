import React, { useEffect, useState } from "react";
import Slider from "react-slick";
import "slick-carousel/slick/slick.css";
import "slick-carousel/slick/slick-theme.css";
import "../styles/VehicleSlider.css";
import { useNavigate } from "react-router-dom";

const API_KEY = "AIzaSyAJ2CZ4UOSpXkonhIwUQMwgZeeDu5g63DA"; // Replace with your actual API Key
const SEARCH_ENGINE_ID = "a7f019b93f51a450b"; // Replace with your actual Search Engine ID

const VehicleSlider = ({ vehicles, matchingScores }) => {
  const [vehicleImages, setVehicleImages] = useState({});

  // Function to standardize color names
  const standardizeColor = (color) => {
    const colorMap = {
      "Midnight Blue": "Blue",
      "Ruby Red": "Red",
      // Add more mappings as needed
    };
    return colorMap[color] || color;
  };

  // Function to fetch vehicle images
  const fetchVehicleImage = async (vehicle) => {
    const { Make, Model, Year, Ext_Color_Generic } = vehicle;
    const color = standardizeColor(Ext_Color_Generic);

    const queries = [
      `${Year} ${color} ${Make} ${Model}`,
      `${Year} ${Make} ${Model}`,
      `${color} ${Make} ${Model}`,
      `${Make} ${Model}`,
    ];

    for (const query of queries) {
      try {
        const params = new URLSearchParams({
          q: query,
          searchType: "image",
          imgType: "photo",
          imgSize: "large",
          num: "1",
          cx: SEARCH_ENGINE_ID,
          key: API_KEY,
        });

        const url = `https://www.googleapis.com/customsearch/v1?${params.toString()}`;
        const response = await fetch(url);
        const data = await response.json();

        if (data.error) {
          console.error("API Error:", data.error);
          return null;
        }

        if (data.items && data.items.length > 0) {
          return data.items[0].link;
        } else {
          console.warn(`No images found for query "${query}".`);
        }
      } catch (error) {
        console.error("Error fetching image:", error);
      }
    }

    return null;
  };

  useEffect(() => {
    if (Array.isArray(vehicles) && vehicles.length > 0) {
      const loadImages = async () => {
        const images = {};
        const imagePromises = vehicles.map(async (vehicle) => {
          // Key generation must match for fetching and retrieval
          const key = `${vehicle.Year}-${vehicle.Make}-${vehicle.Model}-${vehicle.Ext_Color_Generic}`;
          const image =
            (await fetchVehicleImage(vehicle)) ||
            "https://via.placeholder.com/300?text=No+Image+Available";
          images[key] = image;
        });

        await Promise.all(imagePromises);
        setVehicleImages(images);
      };
      loadImages();
    } else {
      console.warn("Vehicles is not an array or is empty.");
    }
  }, [vehicles]);

  const settings = {
    dots: true,
    infinite: true,
    speed: 500,
    slidesToShow: 1,
    slidesToScroll: 1,
  };

  return (
    <div className="vehicle-slider">
      {Array.isArray(vehicles) && vehicles.length > 0 ? (
        <Slider {...settings}>
          {vehicles.map((vehicle, index) => {
            // Key generation for vehicleImages
            const key = `${vehicle.Year}-${vehicle.Make}-${vehicle.Model}-${vehicle.Ext_Color_Generic}`;
            const imageSrc =
              vehicleImages[key] ||
              "https://via.placeholder.com/300?text=Loading...";
            const matchingScore = matchingScores ? matchingScores[index] : 60; // Default to 60 if not provided

            return (
              <div key={index} className="vehicle-card">
                <img
                  src={imageSrc}
                  alt={`${vehicle.Make} ${vehicle.Model}`}
                  className="vehicle-image"
                  onError={(e) => {
                    e.target.src =
                      "https://via.placeholder.com/300?text=No+Image+Available";
                  }}
                />
                <div className="vehicle-info">
                  <h3>{`${vehicle.Year} ${vehicle.Make} ${vehicle.Model}`}</h3>
                  <p>
                    <strong>Body:</strong> {vehicle.Body}
                  </p>
                  <p>
                    <strong>Price:</strong> ${vehicle.SellingPrice}
                  </p>
                  <p>
                    <strong>Miles:</strong> {vehicle.Miles} miles
                  </p>
                  <p>
                    <strong>Color:</strong> {vehicle.Ext_Color_Generic}
                  </p>
                </div>
                <div className="score-circle">
                  <svg viewBox="0 0 36 36" className="circular-chart">
                    <path
                      className="circle-bg"
                      d="M18 2.0845
                       a 15.9155 15.9155 0 0 1 0 31.831
                       a 15.9155 15.9155 0 0 1 0 -31.831"
                    />
                    <path
                      className="circle"
                      strokeDasharray={`${matchingScore}, 100`}
                      d="M18 2.0845
                       a 15.9155 15.9155 0 0 1 0 31.831
                       a 15.9155 15.9155 0 0 1 0 -31.831"
                    />
                  </svg>
                  <span className="score-text">{matchingScore}%</span>
                </div>
              </div>
            );
          })}
        </Slider>
      ) : (
        <div>No vehicles available for display.</div>
      )}
    </div>
  );
};

export default VehicleSlider;
