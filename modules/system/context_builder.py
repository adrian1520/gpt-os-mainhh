import os, json

def build_context():
    context = {
        "status": "READY",
        "system_memory": "active",
        "repo_map": {}
    }
    # Wczytanie indexu z poprzedniego kroku
    if os.path.exists('memory/repo_index.json'):
        with open('memory/repo_index.json', 'r', encoding='utf-8') as f:
            context['repo_map'] = json.load(f)
    os.makedirs('memory', exist_ok=True)
    with open('memory/system_context.json', 'w', encoding='utf-8') as f:
        json.dump(context, f, indent=2)
    print("Context built successfully.")

if __name__ == "__main__":
    build_context()