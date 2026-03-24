import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
BUNDLE_PATH = BASE / "memory/context_bundle.json"
OUTPUT_PATH = BASE / "memory/gpt_context.txt"

MAX_LEN = 5000


def load_bundle():
    if not BUNDLE_PATH.exists():
        raise Exception("⚠ BRAK DANYCH: context_bundle.json missing")

    with open(BUNDLE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def safe_str(text, max_len=300):
    text = str(text)
    return text[:max_len]


def build_context(bundle):

    system = bundle.get("system", {})
    session_log = bundle.get("context", {}).get("session_log", [])
    case = bundle.get("runtime", {}).get("case_memory", {})

    parts = []

    # SYSTEM
    parts.append(f"SYSTEM: {system.get('status')} v{bundle.get('meta', {}).get('version')}")

    # CASE
    if case:
        parts.append("\nCASE:")
        for k, v in case.items():
            parts.append(f"- {k}: {safe_str(v)}")

    # EVENTS
    parts.append("\nEVENTS:")
    for event in session_log[-5:]:
        parts.append(f"- {event.get('event')}")

    # RISK
    if "risk_level" in case:
        parts.append(f"\nRISK: {case.get('risk_level')}")

    context = "\n".join(parts)

    return context[:MAX_LEN]


def save_context(text):
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(text)


def main():
    bundle = load_bundle()
    context = build_context(bundle)
    save_context(context)

    print("✅ GPT CONTEXT BUILT")


if __name__ == "__main__":
    main()
