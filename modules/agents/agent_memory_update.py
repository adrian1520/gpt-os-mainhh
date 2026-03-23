import json
import os

MEMORY_PATH = "memory/system_prompt.json"
INPUT_PATH = "tasks/task.json"

with open(MEMORY_PATH) as f:
    memory = json.load(f)

with open(INPUT_PATH) as f:
    task = json.load(f)

updates = task.get("updates", {})

# apply updates safely
for key, value in updates.items():
    if key in memory.get("memory", {}):
        memory["memory"][key] = value
    elif key in memory:
        memory[key] = value

with open(MEMORY_PATH, "w") as f:
    json.dump(memory, f, indent=2)
