import json
import os
import time
import hashlib

INPUT_PATH = "tasks/task.json"
OUTPUT_DIR = "events"

os.makedirs(OUTPUT_DIR, exist_ok=True)

with open(INPUT_PATH) as f:
    task = json.load(f)

content = task.get("content","").lower()

EVENT_ID = hashlib.sha1(content.encode()).hexdigest()[:12]

type_detected = "other"

if "wniosek" in content:
    type_detected = "wniosek"
elif "apelacj" in content:
    type_detected = "apelacja"
elif "wyrok" in content:
    type_detected = "wyrok"
elif "postanowienie" in content:
    type_detected = "postanowienie"

result = {
    "id": EVENT_ID,
    "timestamp": int(time.time()),
    "type": "parser_typ_pisma",
    "document_type": type_detected
}

filename = f"{OUTPUT_DIR}/event_type_{int(time.time())}.json"

with open(filename,"w") as f:
    json.dump(result,f)
