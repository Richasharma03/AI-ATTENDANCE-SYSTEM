import React, { useRef, useState } from "react";
import Webcam from "react-webcam";
import API from "../api";

const Attendance = () => {
  const webcamRef = useRef(null);
  const [msg, setMsg] = useState("");

  const handlePunch = async () => {
    try {
      console.log("Button clicked");

      // 📍 Get location
      const position = await new Promise((resolve, reject) => {
        navigator.geolocation.getCurrentPosition(resolve, reject);
      });

      const lat = position.coords.latitude;
      const lng = position.coords.longitude;

      console.log("Location:", lat, lng);

      // 📸 Capture image
      const imageSrc = webcamRef.current.getScreenshot();

      const blob = await fetch(imageSrc).then((res) => res.blob());

      const formData = new FormData();
      formData.append("file", blob);
      formData.append("lat", lat);
      formData.append("lng", lng);

      console.log("Sending request...");

      const res = await API.post("/attendance/punch", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      console.log("SUCCESS:", res.data);

      setMsg(res.data.msg || JSON.stringify(res.data));
    } catch (err) {
      console.log("ERROR:", err);
      setMsg(err.response?.data?.detail || "Error occurred");
    }
  };

  return (
    <div style={{ textAlign: "center" }}>
      <h2>AI Attendance System</h2>

      <Webcam
        ref={webcamRef}
        screenshotFormat="image/jpeg"
        width={300}
      />

      <br /><br />

      <button onClick={handlePunch}>Punch</button>

      <p>{msg}</p>
    </div>
  );
};

export default Attendance;