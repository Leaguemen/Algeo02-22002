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
    <div>
      <input type="file" accept="image/*" onChange={handleFileChange} />
      {selectedImage && (
        <img
          src={selectedImage}
          alt="Selected Image"
          style={{ maxWidth: "30%" }}
        />
      )}
    </div>
  );
}

export default ImgButton;
