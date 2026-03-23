import json
import os

EVENTS_DIR = "events"

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

query = os.environ.get("QUERY", "").lower()

answers = []

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

    if "sygnatur" in query:
        answer = f"Sygnatura: {sygn}"
    elif "dat" in query:
        answer = f"Daty: {', '.join(dates)}"
    elif "typ" in query:
        answer = f"Typ pisma: {doc_type}"
    else:
        answer = f"Sprawa {sygn} typu {doc_type}, daty: {', '.join(dates)}"

    answers.append({
        "id": eid,
        "query": query,
        "answer": answer
    })

result = {
    "type": "agent_query",
    "answers": answers,
    "count": len(answers)
}

with open("events/event_query.json", "w") as f:
    json.dump(result, f)
