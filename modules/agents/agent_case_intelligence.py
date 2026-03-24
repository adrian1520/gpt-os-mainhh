
import json

def main():
    try:
        facts = json.load(open("facts.json"))
    except:
        facts = []

    try:
        contradictions = json.load(open("contradictions.json"))
    except:
        contradictions = []

    normalized = [f.get("statement_normalized") for f in facts]

    state = "stable"
    priority = "LOW"
    actions = []

    # 🔥 RULE 1: procedural violation (pełna)
    if "final_decision" in normalized and "delivery_issue" in normalized:
        state = "procedural_violation"
        priority = "CRITICAL"
        actions.append("challenge decision validity")

    # 🔥 RULE 2: suspicious final decision (heurystyka)
    elif "final_decision" in normalized:
        state = "final_decision_detected"
        priority = "MEDIUM"
        actions.append("verify procedural correctness")

    # 🔥 RULE 3: contradictions
    if contradictions:
        state = "evidence_conflict"
        priority = "HIGH"
        actions.append("analyze contradictions")

    out = {
        "legal_state": state,
        "facts_detected": normalized,
        "contradictions": len(contradictions),
        "priority": priority,
        "recommended_actions": actions
    }

    json.dump(out, open("case_intelligence.json", "w"), indent=2)


if __name__ == "__main__":
    main()
