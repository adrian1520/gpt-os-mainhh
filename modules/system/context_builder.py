import os
import json

def build_context():
    context = {
        "status": "READY",
        "system_memory": "active",
        "repo_tree": {}
    }

    if os.path.exists("memory/repo_index.json"):
        with open("memory/repo_index.json", "r", encoding="utf-8") as f:
            context["repo_tree"] = json.load(f)

    os.makedirs("memory", exist_ok=True)
    with open("memory/system_context.json", "w", encoding="utf-8") as f:
        json.dump(context, f, indent=2)

    print("Context with full repo tree built.")

if __name__ == "__main__":
    build_context()
