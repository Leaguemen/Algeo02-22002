import React, { ChangeEvent, useState } from "react";
import logo from "./logo.svg";
import "./App.css";
import Title from "./components/Title";
import ImgButton from "./components/ButtonImg";
import Switch from "./components/switch";

function App() {
  interface PairValue {
    Image: string;
    Val: number;
  }

  interface ResponseData {
    message: string;
    pair_values: PairValue[];
  }
  const [refimage, setRefImage] = useState<string | null>(null);
  const [oriImage, setOriImage] = useState<[string] | null>(null);
  const dataSetImage: string[] = [];
  const [responseData, setResponseData] = useState<ResponseData | null>(null);
  const [processTime, setProcessTime] = useState<number | null>(null);

  // Callback function to update refimage
  const handleRefImageChange = async (newImage: string | null) => {
    setRefImage(newImage);
  };

  const handleToggle = () => {
    setIsChecked(!isChecked);
  };

  const handleDataSetChange = async (e: ChangeEvent<HTMLInputElement>) => {
    dataSetImage.length = 0;
    const selectedFiles = e.target.files;

    if (selectedFiles && selectedFiles.length > 0) {
      for (let i = 0; i < selectedFiles.length; i++) {
        const reader = new FileReader();
        reader.onload = async (event) => {
          if (event.target && typeof event.target.result === "string") {
            dataSetImage.push(event.target.result);
          }

          // Check if all files have been processed
          if (dataSetImage.length === selectedFiles.length) {
            console.log(dataSetImage.length);
            console.log(dataSetImage);
            //sendPostRequest
            await sendPostDataset();
          }
        };

        reader.readAsDataURL(selectedFiles[i]);
      }
      console.log(dataSetImage.length);
    }
  };

  const sendPostDataset = async () => {
    try {
      const response = await fetch("http://127.0.0.1:5000/api/receive", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          data: dataSetImage,
        }),
      });

      if (response.ok) {
        const responseBody = await response.json(); // Parse the response body as JSON
        console.log("POST request successful");
        console.log("Response Body:", responseBody); // Print the response body
      } else {
        console.error("POST request failed");
      }
    } catch (error) {
      console.error("Error:", error);
    }
  };

  const sendPostRefImage = async () => {
    try {
      const startTime = performance.now();
      const response = await fetch("http://127.0.0.1:5000/api/RefImage", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          Ref: refimage,
          Type: isChecked,
        }),
      });

      if (response.ok) {
        const endTime = performance.now();
        setProcessTime(endTime - startTime);
        const responseBody = await response.json(); // Parse the response body as JSON
        setResponseData(responseBody);
        console.log(responseData);
        console.log("POST request successful");
        console.log("Response Body:", responseBody); // Print the response body
      } else {
        console.error("POST request failed");
      }
    } catch (error) {
      console.error("Error:", error);
    }
  };

  const imagesPerPage = 8;
  const [currentPage, setCurrentPage] = useState(1);

  const totalPages = Math.ceil(
    (responseData?.pair_values.length || 0) / imagesPerPage
  );

  const [isChecked, setIsChecked] = useState(false);

  const handleChange = () => {
    setIsChecked(!isChecked);
  };

  const visibleImages = responseData?.pair_values.slice(
    (currentPage - 1) * imagesPerPage,
    currentPage * imagesPerPage
  );

  const handleNextPage = () => {
    if (currentPage < totalPages) {
      setCurrentPage((prev) => prev + 1);
    }
  };

  const handlePrevPage = () => {
    if (currentPage > 1) {
      setCurrentPage((prev) => prev - 1);
    }
  };

  return (
    <div className="App">
      <Title />
      <hr />
      <input
        type="file"
        accept="image/*"
        multiple
        onChange={handleDataSetChange}
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
          display: "inline-block", // Align with the visual style of the button
        }}
      />
      <div className="switch-container">
        <label className="switch">
          <input type="checkbox" onChange={handleChange} />
          <span className="slider"></span>
        </label>
        <span className="switch-label">
          {isChecked ? "By Color" : "By Texture"}
        </span>
      </div>
      <hr />
      <ImgButton onImageChange={handleRefImageChange} />
      <button
        onClick={sendPostRefImage}
        style={{
          cursor: "pointer",
          padding: "5px 10px",
          border: "1px solid #ccc",
          borderRadius: "4px",
          backgroundColor: "#f0f0f0",
        }}
      >
        {" "}
        Search{" "}
      </button>
      <div className="imageGrid">
        {visibleImages &&
          visibleImages.map((item: PairValue, index: number) => (
            <div key={index} className="imageContainer">
              <img
                src={`data:image/jpg;base64,${item.Image}`}
                alt={`Image ${index}`}
              />
              <p>{item.Val}</p>
            </div>
          ))}
      </div>
      <div className="pagination">
        <button onClick={handlePrevPage} disabled={currentPage === 1}>
          Previous
        </button>
        <span>{`Page ${currentPage} of ${totalPages}`}</span>
        <button onClick={handleNextPage} disabled={currentPage === totalPages}>
          Next
        </button>
      </div>
      <div>
        {processTime !== null && (
          <p>Processing time: {processTime.toFixed(2)} milliseconds</p>
        )}
        {responseData && (
          <p>Number of elements: {responseData.pair_values.length}</p>
        )}
      </div>
    </div>
  );
}

export default App;
