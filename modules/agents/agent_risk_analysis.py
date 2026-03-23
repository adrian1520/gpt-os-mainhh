import json
import os
import time

EVENTS_DIR = "events"
OUTPUT_DIR = "events"

files = [f for f in os.listdir(EVENTS_DIR) if f.endswith(".json")]

grouped = {}

for f in files:
    try:
        with open(os.path.join(EVENTS_DIR, f)) as file:
            data = json.load(file)
            eid = data.get("id")
            if not eid:
                continue
            grouped.setdefault(eid, []).append(data)
    except:
        continue

results = []

for eid, events in grouped.items():
    issues = []
    risk = "low"

    has_dates = False
    has_type = False
    has_sygn = False
    has_law = False

    for e in events:
        if e.get("type") == "parser_dates" and e.get("dates"):
            has_dates = True
        if e.get("type") == "parser_typ_pisma":
            has_type = True
        if e.get("type") == "parser_sygnatur":
            has_sygn = True
        if e.get("type") == "agent_law_match" and e.get("results"):
            has_law = True

    if not has_sygn:
        issues.append("brak sygnatury")
    if not has_type:
        issues.append("brak typu pisma")
    if not has_dates:
        issues.append("brak dat")
    if not has_law:
        issues.append("brak dopasowania do prawa")

    if len(issues) >= 3:
        risk = "high"
    elif len(issues) == 2:
        risk = "medium"

    results.append({
        "id": eid,
        "risk_level": risk,
        "issues": issues
    })

result = {
    "timestamp": int(time.time()),
    "type": "agent_risk_analysis",
    "results": results,
    "count": len(results)
}

filename = f"{OUTPUT_DIR}/event_risk_{int(time.time())}.json"

with open(filename, "w") as f:
    json.dump(result, f)
