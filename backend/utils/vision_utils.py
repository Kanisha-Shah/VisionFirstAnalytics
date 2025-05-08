# utils/vision_utils.py
import cv2
import pytesseract
import numpy as np
import re
from ultralytics import YOLO

pytesseract.pytesseract.tesseract_cmd = "tesseract"  # Adjust path if needed
model = YOLO("yolov8n.pt")  # Load pretrained object detection model

def clean_text(text):
    if not text:
        return None
    cleaned = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    return cleaned.strip() if cleaned.strip() else None

def detect_ui_elements_with_yolo(frame):
    """Use YOLO to detect generic UI elements (simulate button detection)."""
    results = model(frame, verbose=False)
    detections = []

    for box in results[0].boxes.data.tolist():
        x1, y1, x2, y2, conf, cls = box
        x, y, w, h = int(x1), int(y1), int(x2 - x1), int(y2 - y1)
        detections.append((x, y, w, h))
    return detections

def extract_text_from_region(frame, region):
    x, y, w, h = region
    roi = frame[y:y+h, x:x+w]
    text = pytesseract.image_to_string(roi, config='--psm 6 -l eng').strip()
    return clean_text(text)

def analyze_frame(frame, frame_number=None):
    print("----Frame Analysis in Progress-----\n")
    result = {
        "frame": frame_number if frame_number is not None else -1,
        "elements": [],
        "actions": [],
        "anomalies": []
    }

    # Resize large screenshots for performance
    height, width = frame.shape[:2]
    if width > 800:
        frame = cv2.resize(frame, (800, int(height * 800 / width)))

    # --- 1. YOLOv8 Object Detection ---
    detections = model.predict(source=frame, imgsz=640, conf=0.3, verbose=False)[0]
    for box in detections.boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        cls_id = int(box.cls[0])
        label = model.names[cls_id]

        result["elements"].append({
            "coords": [x1, y1, x2 - x1, y2 - y1],
            "label": label,
            "confidence": float(box.conf[0])
        })

    # --- 2. OCR (Tesseract) ---
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, 11, 2
    )

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if w < 40 or h < 20 or w/h > 10:
            continue

        roi = frame[y:y+h, x:x+w]
        text = pytesseract.image_to_string(roi, config='--psm 6').strip()

        if text:
            result["elements"].append({
                "coords": [x, y, w, h],
                "text": text,
                "label": "ocr"
            })

    return result
