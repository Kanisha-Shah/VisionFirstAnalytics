# backend/vision_capture.py

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
import base64
import cv2
import numpy as np
import time
import os
import uuid
from utils.vision_utils import analyze_frame 
from tracker_api import session_data, session_last_update

router = APIRouter()
VISION_DIR = "screenshots"
os.makedirs(VISION_DIR, exist_ok=True)

@router.post("/vision/upload")
async def upload_screenshot(request: Request):
    data = await request.json()
    session_id = data.get("session_id")
    image_b64 = data.get("image_base64")
    timestamp = data.get("timestamp")

    if not (session_id and image_b64):
        return JSONResponse(content={"error": "Missing session_id or image_base64"}, status_code=400)

    # Decode base64 to image
    try:
        img_bytes = base64.b64decode(image_b64.split(",")[-1])
        nparr = np.frombuffer(img_bytes, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    except Exception as e:
        return JSONResponse(content={"error": f"Failed to decode image: {str(e)}"}, status_code=500)

    # Save image for inspection (optional)
    filename = f"{session_id}_{uuid.uuid4().hex[:8]}.jpg"
    filepath = os.path.join(VISION_DIR, filename)
    cv2.imwrite(filepath, frame)

    # Run vision analysis
    frame_result = analyze_frame(frame)
    frame_result['timestamp'] = timestamp
    frame_result['source'] = 'vision_capture'
    print("📸 Vision analysis running for frame", filepath)
    print("Result:", frame_result)

    # Merge into session logs
    session_data[session_id].append(frame_result)
    session_last_update[session_id] = time.time()

    return JSONResponse(content={"status": "ok", "frame_insight": frame_result})
