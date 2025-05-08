# backend/main.py
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from tracker_api import router as tracker_router
import cv2
import os
import shutil
import uuid
from utils.vision_utils import analyze_frame
from utils.llm_utils import get_prediction
# from backend.previous_video_logic.behavior_engine import extract_summary
from utils.rule_engine import rule_based_prediction
from utils.vision_capture import router as vision_router
app = FastAPI()

# Enable CORS for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tracker_router)
app.include_router(vision_router)

# UPLOAD_DIR = "uploads"

# @app.post("/upload")
# async def upload_video(file: UploadFile = File(...)):
#     # Save uploaded file
#     file_id = str(uuid.uuid4())
#     upload_path = os.path.join(UPLOAD_DIR, f"{file_id}.mp4")
#     os.makedirs(UPLOAD_DIR, exist_ok=True)

#     with open(upload_path, "wb") as buffer:
#         shutil.copyfileobj(file.file, buffer)

#     # Extract frames
#     frames = extract_frames(upload_path)

#     # Analyze frames
#     insights = []
#     for idx, frame in enumerate(frames):
#         result = analyze_frame(frame, frame_number=idx)
#         insights.append(result)

#     # Summarize behaviors
#     summary = extract_summary(insights)

#     # Get predictions
#     rule_prediction = rule_based_prediction(summary)
#     llm_prediction = get_prediction(summary)

#     return JSONResponse(content={
#         "insights": insights,
#         "summary": summary,
#         "rule_prediction": rule_prediction,
#         "llm_prediction": llm_prediction
#     })
