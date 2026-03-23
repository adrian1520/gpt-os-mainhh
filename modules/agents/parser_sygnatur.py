import json
import os
import re
import time

INPUT_PATH = "tasks/task.json"
OUTPUT_DIR = "events"

os.makedirs(OUTPUT_DIR, exist_ok=True)

with open(INPUT_PATH) as f:
    task = json.load(f)

content = task.get("content","")

match = re.search(r'NSM ?[0-9]+/[0-9]+', content)

result = {
    "timestamp": int(time.time()),
    "type": "parser_sygnatur",
    "sygnatura": match.group(0) if match else None,
    "raw": content[:200]
}

filename = f"{OUTPUT_DIR}/event_{int(time.time())}.json"

with open(filename,"w") as f:
    json.dump(result,f)
