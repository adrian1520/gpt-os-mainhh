from .agent_parser_v4_part1 import *
from .agent_parser_v4_part2 import extract_events, extract_relations, extract_facts

def build_extraction(text: str):
    return {
        "document_type": classify_document(text),
        "signature": extract_signature(text),
        "facts": extract_facts(text),
        "events": extract_events(text),
        "relations": extract_relations(text),
    }