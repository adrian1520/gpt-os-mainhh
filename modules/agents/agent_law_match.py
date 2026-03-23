import json
import os
import time

EVENTS_DIR = "events"
KNOWLEDGE_DIR = "knowledge/kro"
OUTPUT_DIR = "events"

# load law articles
law = []
for f in os.listdir(KNOWLEDGE_DIR):
    try:
        with open(os.path.join(KNOWLEDGE_DIR, f)) as file:
            law.append(json.load(file))
    except:
        continue

# load events
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
    text_blob = ""

    for e in events:
        if "content" in e:
            text_blob += " " + e.get("content","").lower()
        if "sygnatura" in e and e.get("sygnatura"):
            text_blob += " " + e.get("sygnatura","").lower()
        if "document_type" in e and e.get("document_type"):
            text_blob += " " + e.get("document_type","").lower()

    matched = []

    for art in law:
        for kw in art.get("keywords", []):
            if kw.lower() in text_blob:
                matched.append(f"{art.get('code')}_{art.get('article')}")
                break

    results.append({
        "id": eid,
        "matched_articles": list(set(matched))
    })

result = {
    "timestamp": int(time.time()),
    "type": "agent_law_match",
    "results": results,
    "count": len(results)
}

filename = f"{OUTPUT_DIR}/event_law_match_{int(time.time())}.json"

with open(filename, "w") as f:
    json.dump(result, f)
