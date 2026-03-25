import os
import json
import time


BASE_PATH = os.path.join(os.getcwd(), "Legal-os", "cases")


def sanitize(case_id):
    return case_id.replace(" ", "_").replace("/", "_")

def get_case_path(case_id):
    case_clean = sanitize(case_id)
    return os.path.join(BASE_PATH, case_clean)

def get_state_path(case_id):
    return os.path.join(get_case_path(case_id), "case_state.json")

def init_state(case_id):
    return {
        "case_id": case_id,
        "metadata": {
            "created_at": int(time.time()),
            "updated_at": int(time.time())
        },
        "facts": [],
        "timeline": [],
        "entities": [],
        "risk": {},
        "strategy": {},
        "legal_actions": [],
        "documents": [],
        "confidence": 0.0
    }

def load_state(case_id):
    path = get_state_path(case_id)
    if not os.path.exists(path):
        state = init_state(case_id)
        save_state(case_id, state)
        return state
    try:
        with open(path, "r") as f:
            return json.load(f)
    except:
        return init_state(case_id)

def save_state(case_id, state):
    case_path = get_case_path(case_id)
    os.makedirs(case_path, exist_ok=True)
    path = get_state_path(case_id)
    state["metadata"]["updated_at"] = int(time.time())
    with open(path, "w") as f:
        json.dump(state, f, indent=2)

def update_state(case_id, update_fn):
    state = load_state(case_id)
    state = update_fn(state)
    save_state(case_id, state)
    return state