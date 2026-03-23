import json
import os
import time

EVENTS_DIR = "events"
INPUT_PATH = "tasks/task.json"
OUTPUT_DIR = "events"

with open(INPUT_PATH) as f:
    task = json.load(f)

query = task.get("query","").lower()

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

answers = []

for eid, events in grouped.items():
    risk = "unknown"
    issues = []
    actions = []
    law = []

    for e in events:
        if e.get("type") == "agent_risk_analysis":
            for r in e.get("results", []):
                if r.get("id") == eid:
                    risk = r.get("risk_level")
                    issues = r.get("issues", [])

        if e.get("type") == "agent_strategy":
            for r in e.get("results", []):
                if r.get("id") == eid:
                    actions = r.get("recommended_actions", [])

        if e.get("type") == "agent_law_match":
            for r in e.get("results", []):
                if r.get("id") == eid:
                    law = r.get("matched_articles", [])

    answer = ""

    if "ryzyko" in query:
        answer = f"Poziom ryzyka: {risk}. Problemy: {', '.join(issues)}"
    elif "co robić" in query or "co dalej" in query:
        answer = "Zalecane działania: " + ", ".join(actions)
    elif "prawo" in query:
        answer = "Zastosowane przepisy: " + ", ".join(law)
    else:
        answer = f"Sprawa {eid}. Ryzyko: {risk}. Działania: {', '.join(actions)}"

    answers.append({
        "id": eid,
        "answer": answer
    })

result = {
    "type": "agent_chat",
    "answers": answers,
    "count": len(answers)
}

filename = f"{OUTPUT_DIR}/event_chat_{int(time.time())}.json"

with open(filename, "w") as f:
    json.dump(result, f)
