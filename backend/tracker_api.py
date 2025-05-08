# backend/tracker_api.py
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from collections import defaultdict
import time
import uuid
import json
from utils.llm_utils import get_prediction
from utils.rule_engine import rule_based_prediction

router = APIRouter()
session_data = defaultdict(list)
session_last_update = {}
SESSION_TIMEOUT = 30  # seconds

@router.post("/track")
async def track_user_data(request: Request):
    data = await request.json()
    session_id = data.get("session_id") or str(uuid.uuid4())

    session_data[session_id].append(data)
    session_last_update[session_id] = time.time()

    return JSONResponse(content={"status": "ok", "session_id": session_id})

@router.get("/flush")
async def flush_sessions():
    expired_sessions = [sid for sid, ts in session_last_update.items()
                        if time.time() - ts > SESSION_TIMEOUT]
    result = {}

    for sid in expired_sessions:
        summary = summarize_session(session_data[sid])
        llm_pred = get_prediction(summary)
        rule_pred = rule_based_prediction(summary)

        result[sid] = {
            "summary": summary,
            "rule_based_prediction": rule_pred,
            "llm_prediction": llm_pred
        }

        with open("session_logs.txt", "a") as f:
            f.write(f"\n--- SESSION {sid} ---\n")
            f.write(f"{summary}\n\n")

        del session_data[sid]
        del session_last_update[sid]

    return JSONResponse(content=result)

@router.get("/flush/{session_id}")
async def flush_specific_session(session_id: str):
    if session_id not in session_data:
        return JSONResponse(status_code=404, content={"error": "Session not found"})

    summary = summarize_session(session_data[session_id])
    llm_pred = get_prediction(summary)
    rule_pred = rule_based_prediction(summary)

    result = {
        "summary": summary,
        "rule_based_prediction": rule_pred,
        "llm_prediction": llm_pred
    }

    with open("session_logs.txt", "a") as f:
        f.write(f"\n--- SESSION {session_id} ---\n")
        f.write(f"{summary}\n\n")

    print(f"[FLUSH] Triggered for session {session_id}")
    del session_data[session_id]
    del session_last_update[session_id]

    return JSONResponse(content=result)

def summarize_session(events):
    screen_elements = set()
    user_actions = []
    anomalies = []
    cursor_path = []

    for e in events:
        hovered = e.get("hovered_element")
        if hovered:
            tag = hovered.get("tag")
            text = hovered.get("text") or "[no text]"
            disabled = hovered.get("disabled")
            elem_id = hovered.get("id") or ""
            classname = hovered.get("class") or ""

            descriptor = f"{tag}:{text}".strip()
            screen_elements.add(descriptor)

            action_desc = f"Hovered on {tag} '{text}'"
            if disabled:
                action_desc += " (disabled)"
                anomalies.append(f"Hovered on disabled {tag} '{text}'")

            user_actions.append(action_desc)

        cursor = e.get("cursor")
        if cursor:
            cursor_path.append((cursor['x'], cursor['y']))

    timestamps = [e.get("timestamp") for e in events if e.get("timestamp")]
    print(f"--------Summary Generated-------")
    return {
        "screen_elements": list(screen_elements),
        "user_actions": user_actions,
        "anomalies": anomalies,
        "timestamps": timestamps,
        "cursor_path": cursor_path
    }
