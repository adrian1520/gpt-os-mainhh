import json
from pathlib import Path

from modules.system.validate_context_bundle import validate_schema
from modules.system.write_session_log import log_event

BASE = Path(__file__).resolve().parents[2]

BUNDLE_PATH = BASE / "memory/context_bundle.json"


def load_context_bundle():
    if not BUNDLE_PATH.exists():
        raise Exception("⚠ BRAK DANYCH: context_bundle.json missing")

    with open(BUNDLE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def controller(action_fn, *args, **kwargs):
    '''
    Wrapper enforcing memory read + validation + logging
    '''

    # 🔥 LOAD
    context = load_context_bundle()

    # 🔥 VALIDATE
    validate_schema(context)

    # 🔥 LOG START
    log_event("controller_run_start", {
        "action": action_fn.__name__
    })

    print("CONTEXT LOADED & VALID")
    print("Last update:", context.get("meta", {}).get("last_update"))

    try:
        result = action_fn(context, *args, **kwargs)

        # 🔥 LOG SUCCESS
        log_event("controller_run_success", {
            "action": action_fn.__name__
        })

        return result

    except Exception as e:

        # 🔥 LOG ERROR
        log_event("controller_run_error", {
            "action": action_fn.__name__,
            "error": str(e)
        })

        raise


# --- EXAMPLE USAGE ---

def example_action(context, data=None):
    print("Running action with context")
    print("System status:", context.get("system", {}).get("status"))
    return {"status": "ok"}


if __name__ == "__main__":
    controller(example_action)
