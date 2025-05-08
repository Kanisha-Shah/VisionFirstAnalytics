# utils/behavior_engine.py
def extract_summary(frame_insights):
    """
    Aggregate behavior insights across frames.
    Returns a structured summary dict for LLM analysis.
    """
    screen_elements = set()
    user_actions = set()
    anomalies = set()
    timestamps = []

    for frame in frame_insights:
        frame_number = frame.get("frame")
        timestamps.append(frame_number)

        for elem in frame.get("elements", []):
            text = elem.get("text")
            if text:
                screen_elements.add(text.strip())

        for action in frame.get("actions", []):
            user_actions.add(action.strip())

        for anomaly in frame.get("anomalies", []):
            anomalies.add(anomaly.strip())

    return {
        "screen_elements": list(screen_elements),
        "user_actions": list(user_actions),
        "anomalies": list(anomalies),
        "timestamps": timestamps
    }
