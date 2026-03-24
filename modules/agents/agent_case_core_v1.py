# agent_case_core_v1.py

import json
import glob
from datetime import datetime

def load_extractions():
    files = glob.glob("Ekstrakcja_Danych/*.json")
    data = []
    for f in files:
        with open(f, "r", encoding="utf-8") as fh:
            try:
                data.append(json.load(fh))
            except:
                continue
    return data

def merge_documents(extractions):
    return extractions

def merge_entities(extractions):
    entities = []
    for e in extractions:
        entities += e.get("entities", [])
    return entities

def merge_facts(extractions):
    facts = []
    for e in extractions:
        facts += e.get("facts", [])
    return facts

def merge_events(extractions):
    events = []
    for e in extractions:
        events += e.get("events", [])
    try:
        events.sort(key=lambda x: x.get("date",""))
    except:
        pass
    return events

def build_case():
    extractions = load_extractions()

    case = {
        "case_id": "AUTO",
        "documents": merge_documents(extractions),
        "entities": merge_entities(extractions),
        "child": {},
        "facts": merge_facts(extractions),
        "events": merge_events(extractions),
        "timeline": merge_events(extractions),
        "legal_references": [],
        "theses": [],
        "risk_analysis": {},
        "strategy": {},
        "case_state": {
            "phase": "",
            "last_update": datetime.utcnow().isoformat()
        }
    }

    try:
        with open("risk.json","r",encoding="utf-8") as f:
            case["risk_analysis"] = json.load(f).get("risk_analysis",{})
    except:
        pass

    try:
        with open("strategy.json","r",encoding="utf-8") as f:
            case["strategy"] = json.load(f).get("strategy",{})
            case["case_state"]["phase"] = case["strategy"].get("phase","")
    except:
        pass

    return case

def main():
    case = build_case()

    with open("case.json","w","encoding="utf-8") as f:
        json.dump(case,f,indent=2,ensure_ascii=False)

if __name__ == "__main__":
    main()
