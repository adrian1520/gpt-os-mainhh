import json
import os
import time
from datetime import datetime

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

timelines = []

for eid, events in grouped.items():
    timeline = []

    for e in events:
        if e.get("type") == "parser_dates":
            for d in e.get("dates", []):
                timeline.append({
                    "date": d,
                    "source": "parser_dates"
                })

    def parse_date(d):
        try:
            return datetime.strptime(d["date"], "%d.%m.%Y")
        except:
            return datetime.min

    timeline_sorted = sorted(timeline, key=parse_date)

    timelines.append({
        "id": eid,
        "timeline": timeline_sorted
    })

result = {
    "timestamp": int(time.time()),
    "type": "agent_timeline",
    "timelines": timelines,
    "count": len(timelines)
}

filename = f"{OUTPUT_DIR}/event_timeline_{int(time.time())}.json"

with open(filename, "w") as f:
    json.dump(result, f)
