# utils/rule_engine.py
def rule_based_prediction(summary):
    """
    Apply enhanced logic to predict user intent based on the behavior summary.
    """
    actions = summary.get("user_actions", [])
    anomalies = summary.get("anomalies", [])
    screen_elements = summary.get("screen_elements", [])
    cursor_path = summary.get("cursor_path", [])

    # 1. Frustration: repeated interaction with disabled/inactive elements
    if any("inactive" in a.lower() or "disabled" in a.lower() for a in anomalies) and len(actions) >= 2:
        return "Likely frustrated: User clicked multiple inactive or unresponsive buttons."

    # 2. Missing Size Info: user attempts to find sizing guidance
    if any("size" in a.lower() for a in actions) and not any("chart" in e.lower() for e in screen_elements):
        return "Likely searching for size info: Size chart was not found."

    # 3. Confusion: user doesn't interact despite many visible UI elements
    if len(actions) == 0 and len(screen_elements) > 5:
        return "Likely confused: Many elements visible, but no interaction detected."

    # 4. Drop-off: user fills a form but doesn't follow up
    if "Filled form" in actions and "No follow-up action" in anomalies:
        return "Likely drop-off: User filled a form but took no next step."

    # 5. Scroll without interaction (detected via cursor path only)
    if len(cursor_path) > 10 and len(actions) == 0:
        return "Likely passive scroll: User moved through the page without engaging."

    # 6. Repetitive hover on same element
    hover_counts = {}
    for action in actions:
        if "Hovered on" in action:
            key = action.split("Hovered on")[-1].strip()
            hover_counts[key] = hover_counts.get(key, 0) + 1
    for element, count in hover_counts.items():
        if count >= 3:
            return f"Likely stuck: User hovered on '{element}' repeatedly without clicking."

    # 7. Abandoned form: typed but never submitted (heuristic)
    if any("input" in a.lower() or "form" in a.lower() for a in screen_elements) and not any("submit" in a.lower() for a in actions):
        return "Likely form abandonment: Form elements visible, but no submit action detected."

    return "User behavior does not match any predefined rule-based patterns."