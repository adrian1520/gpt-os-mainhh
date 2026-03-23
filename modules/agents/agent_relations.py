import json
import os
import time

EVENTS_DIR = "events"
OUTPUT_DIR = "events"

files = [f for f in os.listdir(EVENTS_DIR) if f.endswith(".json")]

events = []

for f in files:
    try:
        with open(os.path.join(EVENTS_DIR, f)) as file:
            data = json.load(file)
            events.append(data)
    except:
        continue

relations = []

# group by hash-like identifiers if present
by_id = {}

for e in events:
    eid = e.get("id") or e.get("event_id")
    if eid:
        by_id.setdefault(eid, []).append(e)

for eid, group in by_id.items():
    if len(group) > 1:
        for i in range(len(group)-1):
            relations.append({
                "id": eid,
                "from": group[i].get("type"),
                "to": group[i+1].get("type"),
                "relation": "same_entity"
            })

result = {
    "timestamp": int(time.time()),
    "type": "agent_relations",
    "mode": "hash_based",
    "relations": relations,
    "count": len(relations)
}

filename = f"{OUTPUT_DIR}/event_relations_{int(time.time())}.json"

with open(filename,"w") as f:
    json.dump(result,f)
