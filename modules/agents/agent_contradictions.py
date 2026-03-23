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

contradictions = []

for eid, events in grouped.items():
    types = set()
    for e in events:
        if e.get("type") == "parser_typ_pisma":
            types.add(e.get("document_type"))

    if len(types) > 1:
        contradictions.append({
            "id": eid,
            "issue": "multiple_document_types",
            "values": list(types)
        })

result = {
    "timestamp": int(time.time()),
    "type": "agent_contradictions",
    "contradictions": contradictions,
    "count": len(contradictions)
}

filename = f"{OUTPUT_DIR}/event_contradictions_{int(time.time())}.json"

with open(filename, "w") as f:
    json.dump(result, f)
