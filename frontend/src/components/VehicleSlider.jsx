import React from 'react';
import Slider from 'react-slick';
import 'slick-carousel/slick/slick.css';
import 'slick-carousel/slick/slick-theme.css';
import '../styles/VehicleSlider.css'; // Add your custom styling here

const VehicleSlider = ({ vehicles }) => {
  const settings = {
    dots: true,
    infinite: true,
    speed: 500,
    slidesToShow: 1,
    slidesToScroll: 1,
  };

  return (
    <div className="vehicle-slider">
      <Slider {...settings}>
        {vehicles.map((vehicle, index) => (
          <div key={index} className="vehicle-card">
            {/* Placeholder image for vehicle */}
            <img
              src={`https://via.placeholder.com/300?text=${vehicle.Make}+${vehicle.Model}`}
              alt={`${vehicle.Make} ${vehicle.Model}`}
              className="vehicle-image"
            />
            <div className="vehicle-info">
              <h3>{`${vehicle.Year} ${vehicle.Make} ${vehicle.Model}`}</h3>
              <p><strong>Body:</strong> {vehicle.Body}</p>
              <p><strong>Price:</strong> ${vehicle.SellingPrice}</p>
              <p><strong>Miles:</strong> {vehicle.Miles} miles</p>
              <p><strong>Color:</strong> {vehicle.Ext_Color_Generic}</p>
            </div>
          </div>
        ))}
      </Slider>
    </div>
  );
};

export default VehicleSlider;
