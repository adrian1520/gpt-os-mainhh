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
    risk = "low"
    issues = []
    matched_articles = []

    for e in events:
        if e.get("type") == "agent_risk_analysis":
            for r in e.get("results", []):
                if r.get("id") == eid:
                    risk = r.get("risk_level", "low")
                    issues = r.get("issues", [])

        if e.get("type") == "agent_law_match":
            for r in e.get("results", []):
                if r.get("id") == eid:
                    matched_articles = r.get("matched_articles", [])

    steps = []

    if risk == "high":
        steps.append("uzupełnić braki formalne (daty, sygnatura)")
        steps.append("dopasować argumentację do przepisów")
    if "KRO_133" in matched_articles:
        steps.append("przygotować dowody na koszty utrzymania dziecka")
    if "KRO_56" in matched_articles:
        steps.append("udokumentować rozkład pożycia")

    if not steps:
        steps.append("przeanalizować sprawę szczegółowo")

    results.append({
        "id": eid,
        "risk_level": risk,
        "recommended_actions": steps
    })

result = {
    "timestamp": int(time.time()),
    "type": "agent_strategy",
    "results": results,
    "count": len(results)
}

filename = f"{OUTPUT_DIR}/event_strategy_{int(time.time())}.json"

with open(filename, "w") as f:
    json.dump(result, f)
