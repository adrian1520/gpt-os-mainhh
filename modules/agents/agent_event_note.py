import json
import os
import time

INPUT_PATH = "tasks/task.json"
OUTPUT_DIR = "events"

os.makedirs(OUTPUT_DIR, exist_ok=True)

with open(INPUT_PATH) as f:
    task = json.load(f)

nsm = task.get("nsm")
content = task.get("content")
date = task.get("date")

result = {
    "id": nsm,
    "timestamp": int(time.time()),
    "type": "event_note",
    "nsm": nsm,
    "content": content,
    "date": date
}

filename = f"{OUTPUT_DIR}/event_note_{int(time.time())}.json"

with open(filename, "w") as f:
    json.dump(result, f)
