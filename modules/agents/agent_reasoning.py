import json
import os


LAW_PATH = "knowledge/law/kro.json"


def load_law():
    if os.path.exists(LAW_PATH):
        with open(LAW_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def build_reasoning(data):
    law_base = load_law()

    output = {
        "insights": [],
        "risks": [],
        "recommendations": [],
        "score": 0,
        "legal_basis": []
    }

    facts = data.get("facts", [])
    events = data.get("events", [])
    relations = data.get("relations", [])

    score = 0

    # Rule 1: brak doreczenia
    if any("brak doreczenia" in f.get("content", "") for f in facts):
        output["risks"].append("Naruszenie procedury (doreczenie)")
        output["recommendations"].append("Sprawd doreczenie dokumentów")
        score += 2

        if "art.97" in law_base:
            output["legal_basis"].append("oparte o art.97 KRO")

    # Rule 2: ograniczenie władzq
    if any("ograniczenie" in f.get("content", "") for f in facts):
        output["risks"].append("Wysokie rizyko utraty władzq")
        output["recommendations"].append("Przygotuj obrone praw rodziciela")
        score += 3

        if "art.107" in law_base:
            output["legal_basis"].append("oparte o art.107 KRO")

    # Rule 3: context sprawy
    if len(events) > 1:
        output["insights"].append("Eskalacja sprawy (wiele zdarzeő)")
        score += 2

    if relations:
        output["insights"].append("Sprawa rodzinna (tryb KRO)")

    # Scoring final
    output["score"] = score

    return output