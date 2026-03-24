import json
from pathlib import Path
from datetime import datetime

BASE = Path(__file__).resolve().parents[2]

SESSION_LOG_PATH = BASE / "memory/session_log.json"
LIVE_SESSION_PATH = BASE / "memory/live_session.json"


def load_json(path, default):
    if not path.exists():
        return default
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def log_event(event_type, details=None):
    timestamp = datetime.utcnow().isoformat()

    # --- session log ---
    session_log = load_json(SESSION_LOG_PATH, [])

    event = {
        "timestamp": timestamp,
        "event": event_type,
        "details": details or {}
    }

    session_log.append(event)
    save_json(SESSION_LOG_PATH, session_log)

    # --- live session ---
    live_session = load_json(LIVE_SESSION_PATH, {})

    live_session["current_step"] = event_type
    live_session["last_action"] = details.get("action") if details else event_type
    live_session["last_update"] = timestamp

    save_json(LIVE_SESSION_PATH, live_session)

    return event


# --- TEST ---
if __name__ == "__main__":
    log_event("test_event", {"action": "test_run"})
