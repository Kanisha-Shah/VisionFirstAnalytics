# utils/video_utils.py
import cv2
import os
import uuid

def extract_frames(video_path, frame_rate=1):
    """
    Extract frames from video at the given frame rate (1 frame/sec default).
    Saves frames to 'frames' directory and returns a list of frame images (as numpy arrays).
    """
    cap = cv2.VideoCapture(video_path)
    frames = []
    count = 0
    frame_index = 0
    session_id = str(uuid.uuid4())
    output_dir = os.path.join("./frames", session_id)
    os.makedirs(output_dir, exist_ok=True)

    if not cap.isOpened():
        raise IOError(f"Cannot open video {video_path}")

    fps = cap.get(cv2.CAP_PROP_FPS)
    interval = int(fps * frame_rate)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if count % interval == 0:
            frame_path = os.path.join(output_dir, f"frame_{frame_index}.jpg")
            cv2.imwrite(frame_path, frame)
            frames.append(frame)
            frame_index += 1

        count += 1

    cap.release()
    return frames