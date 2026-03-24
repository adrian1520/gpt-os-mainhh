import json

MAX_CHARS = 5000

def load_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def compress_text(text, limit=MAX_CHARS):
    if len(text) <= limit:
        return text
    return text[:limit] + "...[TRIMMED]"

def build_gpt_context():
    system_context = load_json("memory/system_context.json")
    case_memory = load_json("memory/case_memory.json")
    context_bundle = load_json("memory/context_bundle.json")
    session_log = load_json("memory/session_log.json")

    prompt = {
        "system": system_context,
        "case": case_memory,
        "context": context_bundle,
        "session": session_log[-5:]
    }

    prompt_str = json.dumps(prompt, indent=2)
    prompt_str = compress_text(prompt_str)

    return prompt_str

if __name__ == "__main__":
    print(build_gpt_context())
