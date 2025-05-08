// src/VideoUploader.js
import React, { useState } from "react";
import axios from "axios";

export default function VideoUploader() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await axios.post("http://localhost:8000/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setResult(response.data);
    } catch (err) {
      console.error("Upload failed", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: "20px", fontFamily: "Arial" }}>
      <h2>Upload a Video for Vision-First Analysis</h2>
      <input type="file" accept="video/*" onChange={(e) => setFile(e.target.files[0])} />
      <br /><br />
      <button onClick={handleUpload} disabled={loading}>
        {loading ? "Uploading..." : "Upload & Analyze"}
      </button>

      {result && (
        <div style={{ marginTop: "20px" }}>
          <h3>🔍 Raw Frame Insights:</h3>
          <pre style={{ background: "#f0f0f0", padding: "10px" }}>{JSON.stringify(result.insights, null, 2)}</pre>

          <h3>🧠 Behavior Summary (Parsed):</h3>
          <pre style={{ background: "#f8f8f8", padding: "10px" }}>{JSON.stringify(result.summary, null, 2)}</pre>

          <h3>🧠 Prediction Output (LLM-Based):</h3>
          <p style={{ background: "#e6ffe6", padding: "10px" }}>{result.llm_prediction}</p>
        </div>
      )}
    </div>
  );
}
