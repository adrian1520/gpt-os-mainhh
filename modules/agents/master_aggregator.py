import json
import os
import time

OUTPUT_DIR = "Legal-os/Outputs"

def load_json(path):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except:
        return {}

def main():
    files = os.listdir(OUTPUT_DIR) if os.path.exists(OUTPUT_DIR) else []

    case = {}
    facts = {}
    strategy = {}
    risk = {}
    legal = {}

    for f in files:
        path = os.path.join(OUTPUT_DIR, f)

        if "case" in f:
            case = load_json(path)
        elif "facts" in f:
            facts = load_json(path)
        elif "strategy" in f:
            strategy = load_json(path)
        elif "risk" in f:
            risk = load_json(path)
        elif "legal_action" in f:
            legal = load_json(path) if f.endswith(".json") else {"text": open(path).read()}

    final = {
        "timestamp": int(time.time()),
        "type": "master_aggregator",
        "case": case,
        "facts": facts,
        "strategy": strategy,
        "risk": risk,
        "legal_action": legal,
        "summary": {
            "has_case": bool(case),
            "has_facts": bool(facts),
            "has_strategy": bool(strategy),
            "has_risk": bool(risk),
            "has_legal_action": bool(legal)
        }
    }

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    out_path = os.path.join(OUTPUT_DIR, f"final_case_{int(time.time())}.json")

    with open(out_path, "w") as f:
        json.dump(final, f)

    print("MASTER AGGREGATOR DONE")

if __name__ == "__main__":
    main()
