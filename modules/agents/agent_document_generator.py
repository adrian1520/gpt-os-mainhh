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
    sygn = eid
    actions = []
    facts = []

    for e in events:
        if e.get("type") == "agent_strategy":
            for r in e.get("results", []):
                if r.get("id") == eid:
                    actions = r.get("recommended_actions", [])

        if e.get("type") == "event_note":
            facts.append(e.get("content"))

    doc = f"Sygnatura: {sygn}\n\n"

    doc += "Stan faktyczny:\n"
    for fct in facts:
        doc += f"- {fct}\n"

    doc += "\nWnioski i działania:\n"
    for act in actions:
        doc += f"- {act}\n"

    results.append({
        "id": eid,
        "document": doc
    })

result = {
    "timestamp": int(time.time()),
    "type": "agent_document",
    "results": results,
    "count": len(results)
}

filename = f"{OUTPUT_DIR}/event_document_{int(time.time())}.json"

with open(filename, "w") as f:
    json.dump(result, f)
