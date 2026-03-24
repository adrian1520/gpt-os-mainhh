import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
BUNDLE_PATH = BASE / "memory/context_bundle.json"


def load_bundle():
    if not BUNDLE_PATH.exists():
        raise Exception("⚠ BRAK DANYCH: context_bundle.json missing")

    with open(BUNDLE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def validate_schema(bundle):
    required_keys = ["system", "knowledge", "context", "runtime", "meta"]

    for key in required_keys:
        if key not in bundle:
            raise Exception(f"❌ SCHEMA ERROR: missing key '{key}'")

    if not isinstance(bundle["context"].get("system_context", {}), dict):
        raise Exception("❌ system_context must be dict")

    if not isinstance(bundle["context"].get("session_log", []), list):
        raise Exception("❌ session_log must be list")

    return True


def main():
    bundle = load_bundle()
    validate_schema(bundle)
    print("✅ CONTEXT VALID")


if __name__ == "__main__":
    main()
