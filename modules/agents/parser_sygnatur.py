import json
import os
import re
import time
import hashlib

INPUT_PATH = "tasks/task.json"
OUTPUT_DIR = "events"

os.makedirs(OUTPUT_DIR, exist_ok=True)

with open(INPUT_PATH) as f:
    task = json.load(f)

content = task.get("content","")

EVENT_ID = hashlib.sha1(content.encode()).hexdigest()[:12]

match = re.search(r'NSM ?[0-9]+/[0-9]+', content)

result = {
    "id": EVENT_ID,
    "timestamp": int(time.time()),
    "type": "parser_sygnatur",
    "sygnatura": match.group(0) if match else None
}

filename = f"{OUTPUT_DIR}/event_sygn_{int(time.time())}.json"

with open(filename,"w") as f:
    json.dump(result,f)
