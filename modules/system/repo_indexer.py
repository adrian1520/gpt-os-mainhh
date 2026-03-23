import os, json

def generate_index():
    index = {}
    for root, dirs, files in os.walk('.'):
        # Ignoruj foldery systemowe
        if '.git' in root or '__pycache__' in root:
            continue

        path = root.replace('.\\', '').replace('./', '')
        if path == '.':
            path = 'root'

        index[path] = files

    os.makedirs('memory', exist_ok=True)
    with open('memory/repo_index.json', 'w', encoding='utf-8') as f:
        json.dump(index, f, indent=2)
    print("Wygenerowano repo_index.json")

if __name__ == "__main__":
    generate_index()
