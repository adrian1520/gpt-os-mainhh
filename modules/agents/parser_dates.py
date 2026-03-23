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

dates = re.findall(r'[0-9]{1,2}\.[0-9]{1,2}\.[0-9]{4}', content)

result = {
    "id": EVENT_ID,
    "timestamp": int(time.time()),
    "type": "parser_dates",
    "dates": dates,
    "count": len(dates)
}

filename = f"{OUTPUT_DIR}/event_dates_{int(time.time())}.json"

with open(filename,"w") as f:
    json.dump(result,f)
