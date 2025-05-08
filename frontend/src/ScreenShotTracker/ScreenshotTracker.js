// src/ScreenshotTracker.js
import { useEffect } from "react";
import html2canvas from "html2canvas";

const ScreenshotTracker = () => {
  useEffect(() => {
    const sessionId = localStorage.getItem("session_id") || crypto.randomUUID();
    localStorage.setItem("session_id", sessionId);

    const intervalId = setInterval(() => {
      html2canvas(document.body, {
        useCORS: true,
        logging: false,
        allowTaint: true,
        windowWidth: document.documentElement.scrollWidth,
        windowHeight: document.documentElement.scrollHeight,
        scrollX: 0,
        scrollY: 0,
        scale: 1
      }).then(canvas => {
        const base64Image = canvas.toDataURL("image/jpeg");

        fetch("http://localhost:8000/vision/upload", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            session_id: sessionId,
            image_base64: base64Image,
            timestamp: new Date().toISOString()
          })
        }).then(() => {
          console.log("📸 Screenshot sent");
        }).catch(err => {
          console.error("Screenshot error", err);
        });
      });
    }, 5000);

    return () => clearInterval(intervalId); // cleanup on unmount
  }, []);

  return null; // This component doesn't render anything
};

export default ScreenshotTracker;