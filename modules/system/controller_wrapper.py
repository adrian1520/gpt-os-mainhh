import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]

BUNDLE_PATH = BASE / "memory/context_bundle.json"


def load_context_bundle():
    if not BUNDLE_PATH.exists():
        raise Exception("⚠ BRAK DANYCH: context_bundle.json missing")

    with open(BUNDLE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def controller(action_fn, *args, **kwargs):
    '''
    Wrapper enforcing memory read before execution
    '''

    # 🔥 HARD ENFORCEMENT
    context = load_context_bundle()

    print("CONTEXT LOADED")
    print("Last update:", context.get("meta", {}).get("last_update"))

    # pass context into action
    result = action_fn(context, *args, **kwargs)

    return result


# --- EXAMPLE USAGE ---

def example_action(context, data=None):
    print("Running action with context")
    print("System status:", context.get("system", {}).get("status"))
    return {"status": "ok"}


if __name__ == "__main__":
    controller(example_action)
