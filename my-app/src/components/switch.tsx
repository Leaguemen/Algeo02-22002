import React, { useState, ChangeEvent } from "react";
import "./Switch.css";

interface SwitchProps {
  isChecked: boolean;
  onToggle: () => void;
}

const Switch: React.FC<SwitchProps> = () => {
  const [isChecked, setIsChecked] = useState(false);

  const handleChange = () => {
    setIsChecked(!isChecked);
  };

  return (
    <div className="switch-container">
      <label className="switch">
        <input type="checkbox" onChange={handleChange} />
        <span className="slider"></span>
      </label>
      <span className="switch-label">
        {isChecked ? "By Color" : "By Texture"}
      </span>
    </div>
  );
};

export default Switch;
