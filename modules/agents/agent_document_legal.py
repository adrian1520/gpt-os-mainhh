import json
import os
import time

EVENTS_DIR = "events"
TEMPLATE_PATH = "templates/wniosek_kontakty_babcia.txt"
OUTPUT_DIR = "events"

# load template
with open(TEMPLATE_PATH, "r") as f:
    template = f.read()

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
    facts = []
    actions = []

    for e in events:
        if e.get("type") == "event_note":
            facts.append(e.get("content"))

        if e.get("type") == "agent_strategy":
            for r in e.get("results", []):
                if r.get("id") == eid:
                    actions = r.get("recommended_actions", [])

    stan_faktyczny = "\n".join(facts)
    propozycja = "\n".join(actions)

    doc = template
    doc = doc.replace("{{sygnatura}}", sygn)
    doc = doc.replace("{{wnioskodawca}}", "WNIOKODAWCA_DO_UZUPEŁNIENIA")
    doc = doc.replace("{{uczestnik}}", "UCZESTNIK_DO_UZUPEŁNIENIA")
    doc = doc.replace("{{dziecko}}", "DANE_DZIECKA")
    doc = doc.replace("{{stan_faktyczny}}", stan_faktyczny)
    doc = doc.replace("{{propozycja_kontaktów}}", propozycja)

    results.append({
        "id": eid,
        "document": doc
    })

result = {
    "timestamp": int(time.time()),
    "type": "legal_document",
    "results": results,
    "count": len(results)
}

filename = f"{OUTPUT_DIR}/event_legal_document_{int(time.time())}.json"

with open(filename, "w") as f:
    json.dump(result, f)
