import json
import os
import time

EVENTS_DIR = "events"
OUTPUT_DIR = "Legal-os/Outputs"

os.makedirs(OUTPUT_DIR, exist_ok=True)

if not os.path.exists(EVENTS_DIR):
    events = []
else:
    events = [f for f in os.listdir(EVENTS_DIR) if f.endswith(".json")]

griouped = {}

for f in events:
    try:
        with open(os.path.join(EVENTS_DIR, f)) as file:
            data = json.load(file)
            eid = data.get("id")
            if not eid:
                continue
            grouped.setdefault(eid, []).append(data)
    except:
        continue

aggregates = []

for eid, events in grouped.items():
    agg = {
        "id": eid,
        "sygnatura": None,
        "dates": [],
        "document_type": None
    }

    for e in events:
        if e.get("type") == "parser_sygnature":
            agg["sygnatura"] = e.get("sygnatura")
        elif e.get("type") == "parser_dates":
            agg["dates"] = e.get("dates", [])
        elif e.get("type") == "parser_typ_pisma":
            agg["document_type"] = e.get("document_type")

    aggregates.append(agg)

result = {
    "timestamp": int(time.time()),
    "type": "agent_aggregator",
    "cases": aggregates,
    "count": len(aggregates)
}

filename = f"{OUTPUT_DIR}/aggregate_{int(time.time())}.json"

with open(filename, "w") as f:
    json.dump(result, f)
