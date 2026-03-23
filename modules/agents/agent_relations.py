import json
import os
import time

EVENTS_DIR = "events"
OUTPUT_DIR = "events"

files = [f for f in os.listdir(EVENTS_DIR) if f.endswith(".json")]

relations = []

events = []

for f in files:
    try:
        with open(os.path.join(EVENTS_DIR, f)) as file:
            data = json.load(file)
            events.append(data)
    except:
        continue

events_sorted = sorted(events, key=lambda x: x.get("timestamp",0))

for i in range(len(events_sorted)-1):
    e1 = events_sorted[i]
    e2 = events_sorted[i+1]

    if abs(e1.get("timestamp",0) - e2.get("timestamp",0)) < 5:
        relations.append({
            "from": e1.get("type"),
            "to": e2.get("type"),
            "relation": "same_input"
        })

result = {
    "timestamp": int(time.time()),
    "type": "agent_relations",
    "relations": relations,
    "count": len(relations)
}

filename = f"{OUTPUT_DIR}/event_relations_{int(time.time())}.json"

with open(filename,"w") as f:
    json.dump(result,f)
