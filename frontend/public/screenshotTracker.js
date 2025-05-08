// public/screenshotTracker.js

(function () {
    const sessionId = localStorage.getItem("session_id") || crypto.randomUUID();
    localStorage.setItem("session_id", sessionId);
  
    function sendScreenshot(imageBase64) {
      fetch("http://localhost:8000/vision/upload", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          session_id: sessionId,
          timestamp: new Date().toISOString(),
          image_base64: imageBase64
        })
      })
      .then(res => res.json())
      .then(data => console.log("Screenshot Sent:", data))
      .catch(err => console.error("Screenshot upload failed", err));
    }
  
    function captureAndSend() {
        if (window.html2canvas) {
          html2canvas(document.body, {
            useCORS: true,
            allowTaint: true,
            logging: false,
            windowWidth: document.documentElement.scrollWidth,
            windowHeight: document.documentElement.scrollHeight,
            scrollX: 0,
            scrollY: 0,
            scale: 1
          }).then(canvas => {
            const imageData = canvas.toDataURL("image/jpeg");
            sendScreenshot(imageData);
          }).catch(err => {
            console.error("Screenshot capture failed:", err);
          });
        } else {
          console.warn("html2canvas is not loaded.");
        }
      }
  
    setInterval(captureAndSend, 5000); // every 5 seconds
  })();
  