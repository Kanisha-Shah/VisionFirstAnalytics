(function () {
    const sessionId = localStorage.getItem("session_id") || crypto.randomUUID();
    localStorage.setItem("session_id", sessionId);
  
    let lastHovered = null;
    let lastActivity = Date.now();
    const FLUSH_TIMEOUT = 10000; // 10s
  
    document.addEventListener("mousemove", () => {
      lastActivity = Date.now();
    });
  
    function getHoveredElementData() {
      if (!lastHovered) return null;
      return {
        tag: lastHovered.tagName,
        text: lastHovered.innerText?.trim().slice(0, 100),
        disabled: lastHovered.disabled || false,
        id: lastHovered.id || null,
        class: lastHovered.className || null,
      };
    }
  
    function getVisibleTextSummary() {
      const tags = ["button", "input", "form", "textarea", "select", "label", "div"];
      const texts = [];
      tags.forEach(tag => {
        document.querySelectorAll(tag).forEach(el => {
          const txt = el.innerText || el.value;
          if (txt && txt.trim().length > 2) {
            texts.push(`${tag}: ${txt.trim().slice(0, 100)}`);
          }
        });
      });
      return texts;
    }
  
    function sendData(data) {
      navigator.sendBeacon("http://localhost:8000/track", JSON.stringify(data));
    }
  
    document.addEventListener("mousemove", (e) => {
      const el = document.elementFromPoint(e.clientX, e.clientY);
      if (el && el !== lastHovered) {
        lastHovered = el;
      }
    });
  
    setInterval(() => {
      const data = {
        session_id: sessionId,
        timestamp: new Date().toISOString(),
        cursor: {
          x: window.event?.clientX || 0,
          y: window.event?.clientY || 0,
        },
        hovered_element: getHoveredElementData(),
        visible_text: getVisibleTextSummary(),
        dom_snapshot: document.body.outerHTML?.slice(0, 10000),
        screen_url: window.location.href
      };
      sendData(data);
    }, 1000);
  
    function checkInactivityAndFlush() {
      const now = Date.now();
      if (now - lastActivity >= FLUSH_TIMEOUT) {
        flushSession(); // call below function
        lastActivity = now + 999999; // prevent more flushes
      }
    }
  
    function flushSession() {
      fetch(`http://localhost:8000/flush/${sessionId}`)
        .then(res => res.json())
        .then(data => {
          console.log("Flush Result:", data);
          displayLLMPrediction(data);
        })
        .catch(err => console.error("Flush failed", err));
    }
  
    function displayLLMPrediction(data) {
      const el = document.createElement("div");
      el.style.position = "fixed";
      el.style.bottom = "20px";
      el.style.right = "20px";
      el.style.padding = "10px";
      el.style.backgroundColor = "rgba(0,0,0,0.8)";
      el.style.color = "#fff";
      el.style.fontSize = "14px";
      el.style.maxWidth = "300px";
      el.style.zIndex = 9999;
      el.innerText = JSON.stringify(data, null, 2);
      document.body.appendChild(el);
    }
  
    // function createFlushNowButton() {
    //   const button = document.createElement("button");
    //   button.innerText = "🚀 Flush Now (Debug)";
    //   button.style.position = "fixed";
    //   button.style.bottom = "80px";
    //   button.style.right = "20px";
    //   button.style.padding = "10px";
    //   button.style.backgroundColor = "#007bff";
    //   button.style.color = "#fff";
    //   button.style.border = "none";
    //   button.style.borderRadius = "5px";
    //   button.style.cursor = "pointer";
    //   button.style.zIndex = 9999;
  
    //   button.addEventListener("click", flushSession);
    //   document.body.appendChild(button);
    // }
  
    setInterval(checkInactivityAndFlush, 3000);
    // createFlushNowButton();
  })();