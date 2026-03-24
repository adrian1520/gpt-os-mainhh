import json
from datetime import datetime
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]

def read_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def read_text(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except:
        return ""

def main():

    bundle = {
        "system": {},
        "knowledge": {},
        "context": {},
        "runtime": {},
        "meta": {}
    }

    # SYSTEM
    system_context = read_json(BASE / "memory/system_context.json")
    bundle["system"] = {
        "status": system_context.get("status")
    }

    # KNOWLEDGE
    knowledge = read_text(BASE / "knowledge/system_knowledge.md")
    bundle["knowledge"] = {
        "system_knowledge": knowledge[:5000]
    }

    # CONTEXT
    bundle["context"] = {
        "system_context": system_context,
        "session_log": read_json(BASE / "memory/session_log.json")
    }

    # RUNTIME
    bundle["runtime"] = {
        "live_session": read_json(BASE / "memory/live_session.json"),
        "case_memory": read_json(BASE / "memory/case_memory.json")
    }

    # META
    bundle["meta"] = {
        "last_update": datetime.utcnow().isoformat(),
        "version": "1.0"
    }

    # SAVE
    output_path = BASE / "memory/context_bundle.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(bundle, f, ensure_ascii=False, indent=2)

    print("CONTEXT BUNDLE BUILT")

if __name__ == "__main__":
    main()
