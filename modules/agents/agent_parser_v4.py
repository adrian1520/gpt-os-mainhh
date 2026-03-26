from modules.agents.agent_parser_v4_part1 import *
from modules.agents.agent_parser_v4_part2 import extract_events, extract_relations, extract_facts

def build_extraction(text: str):
    return {
        "document_type": classify_document(text),
        "signature": extract_signature(text),
        "facts": extract_facts(text),
        "events": extract_events(text),
        "relations": extract_relations(text),
    }

if __name__ == "__main__":
    import sys, json
    text = sys.stdin.read()
    try:
        result = build_extraction(text)
        print(json.dumps(result))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
