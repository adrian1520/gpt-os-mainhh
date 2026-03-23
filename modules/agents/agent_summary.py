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

summaries = []

for eid, events in grouped.items():
    sygn = None
    dates = []
    doc_type = None

    for e in events:
        if e.get("type") == "parser_sygnatur":
            sygn = e.get("sygnatura")
        elif e.get("type") == "parser_dates":
            dates = e.get("dates", [])
        elif e.get("type") == "parser_typ_pisma":
            doc_type = e.get("document_type")

    summary_text = f"Sprawa {sygn or 'brak sygnatury'} typu {doc_type or 'nieznany'}."

    if dates:
        summary_text += f" Kluczowe daty: {', '.join(dates)}."

    summaries.append({
        "id": eid,
        "summary": summary_text
    })

result = {
    "timestamp": int(time.time()),
    "type": "agent_summary",
    "summaries": summaries,
    "count": len(summaries)
}

filename = f"{OUTPUT_DIR}/event_summary_{int(time.time())}.json"

with open(filename, "w") as f:
    json.dump(result, f)
