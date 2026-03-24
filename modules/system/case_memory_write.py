import json
from pathlib import Path
from datetime import datetime

BASE = Path(__file__).resolve().parents[2]

CASE_MEMORY_PATH = BASE / "memory/case_memory.json"


def load_case():
    if not CASE_MEMORY_PATH.exists():
        return {}
    with open(CASE_MEMORY_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_case(data):
    with open(CASE_MEMORY_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def update_case(section: str, payload: dict):
    case = load_case()

    if section not in case:
        case[section] = {}

    case[section].update(payload)

    case["last_update"] = datetime.utcnow().isoformat()

    save_case(case)

    return case


def write_facts(facts: list):
    return update_case("facts", {"items": facts})


def write_law(laws: list):
    return update_case("law", {"articles": laws})


def write_risk(level: str, reason: str):
    return update_case("risk", {
        "level": level,
        "reason": reason
    })


def write_strategy(strategy: str):
    return update_case("strategy", {
        "plan": strategy
    })


if __name__ == "__main__":
    write_facts(["kontakt odrzucony", "brak wydania dziecka"])
    write_risk("HIGH", "powtarzalność naruszeń")
