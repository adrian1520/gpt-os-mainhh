from modules.agents.agent_parser_v4_part1 import *
from modules.agents.agent_parser_v4_part2 import extract_events, extract_relations, extract_facts

def safe(fn, text):
    try:
        return fn(text)
    except Exception as e:
        return {"error": str(e)}

def build_extraction(text: str):
    text = text or ""
    return {
        "document_type": safe(classify_document, text),
        "signature": safe(extract_signature, text),
        "facts": safe(extract_facts, text),
        "events": safe(extract_events, text),
        "relations": safe(extract_relations, text),
    }

def main():
    import sys, json
    text = sys.stdin.read() or ""
    try:
        result = build_extraction(text)
        print(json.dumps(result))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
    import sys
    sys.exit(0)

if __name__ == "__main__":
    main()

main()
