import os
import json
import subprocess

def generate_index():
    try:
        result = subprocess.run(
            ["git", "ls-tree", "-r", "--name-only", "HEAD"],
            capture_output=True,
            text=True,
            check=True
        )
        files = result.stdout.splitlines()

        tree = {}
        for file_path in files:
            parts = file_path.split("/")
            current = tree
            for part in parts[:-1]:
                current = current.setdefault(part, {})
            current.setdefault("files", []).append(parts[-1])

        os.makedirs("memory", exist_ok=True)
        with open("memory/repo_index.json", "w", encoding="utf-8") as f:
            json.dump(tree, f, indent=2)

        print("Full repo tree indexed.")
    except Exception as e:
        print("Indexing failed:", str(e))

if __name__ == "__main__":
    generate_index()
