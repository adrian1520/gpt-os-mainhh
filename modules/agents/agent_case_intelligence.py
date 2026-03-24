
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

    state = "stable"
    if contradictions:
        state = "conflict"

    out = {
        "legal_state": state,
        "contradictions": len(contradictions),
        "recommended_action": "analyze contradictions" if contradictions else "monitor"
    }

    json.dump(out, open("case_intelligence.json","w"), indent=2)

if __name__ == "__main__":
    main()
