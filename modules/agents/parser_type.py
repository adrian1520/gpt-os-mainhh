import json
import os
import re
import time

INPUT_PATH = "tasks/task.json"
OUTPUT_DIR = "events"

os.makedirs(OUTPUT_DIR, exist_ok=True)

with open(INPUT_PATH) as f:
    task = json.load(f)

content = task.get("content","").lower()

type_detected = "other"

if "wniosek" in content:
    type_detected = "wniosek
elif "apelacj" in content:
    type_detected = "apelacja"
elif "wyrok" in content:
    type_detected = "wyrok"
elif "postanowienie" in content:
    type_detected = "postanowienie"

result = {
    "timestamp": int(time.time()),
    "type": "parser_typ_pisma",
    "document_type": type_detected
}

filename = f"{OUTPUT_DIR}/event_type_{int(time.time())}.json"

with open(filename,"w") as f:
    json.dump(result,f)
