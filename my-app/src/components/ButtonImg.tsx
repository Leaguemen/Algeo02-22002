import React, { ChangeEvent, useState } from "react";

interface ImgButtonProps {
  onImageChange: (newImage: string | null) => void;
}

function ImgButton({ onImageChange }: ImgButtonProps) {
  const [selectedImage, setSelectedImage] = useState<string | null>(null);

  const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
    const selectedFiles = e.target.files;
    if (selectedFiles && selectedFiles.length > 0) {
      const reader = new FileReader();
      reader.onload = (e) => {
        if (e.target && typeof e.target.result === "string") {
          setSelectedImage(e.target.result);
          // Call the callback to update refimage in App.tsx
          onImageChange(e.target.result);
        }
      };
      reader.readAsDataURL(selectedFiles[0]);
    }
  };

  return (
    <div
      style={{ marginBottom: "20px", marginTop: "20px", textAlign: "center" }}
    >
      {selectedImage && (
        <img
          src={selectedImage}
          alt="Selected Image"
          style={{ maxWidth: "100%", marginTop: "10px", borderRadius: "8px" }}
        />
      )}
      <label
        htmlFor="imageInput"
        style={{
          cursor: "pointer",
          padding: "10px",
          border: "2px solid #3498db",
          borderRadius: "8px",
          backgroundColor: "#3498db",
          color: "#fff",
          fontWeight: "bold",
          fontSize: "16px",
          marginTop: "10px",
        }}
      >
        Choose Image
        <input
          type="file"
          id="imageInput"
          accept="image/*"
          onChange={handleFileChange}
          style={{ display: "none" }}
        />
      </label>
    </div>
  );
}

export default ImgButton;
