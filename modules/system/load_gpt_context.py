from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
CONTEXT_PATH = BASE / "memory/gpt_context.txt"


def load_context():
    if not CONTEXT_PATH.exists():
        return "⚠ BRAK KONTEKSTU"

    with open(CONTEXT_PATH, "r", encoding="utf-8") as f:
        return f.read()


def build_prompt(user_input: str):

    context = load_context()

    prompt = f"""
SYSTEM CONTEXT:
{context}

---

USER INPUT:
{user_input}

---

INSTRUCTION:
Use system context. Be precise. Act as Legal OS.
"""

    return prompt


if __name__ == "__main__":
    print(build_prompt("Test input"))
