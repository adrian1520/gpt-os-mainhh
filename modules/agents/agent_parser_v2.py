# agent_parser_v2.py

import re
import json
from datetime import datetime

def extract_signature(text):
    match = re.search(r'[IVX]+ Nsm \d+/\d+', text)
    return match.group(0) if match else None

def classify_document(text):
    if "Wnoszę o" in text:
        return "wniosek"
    if "postanawia" in text:
        return "postanowienie"
    if "wzywa" in text:
        return "wezwanie"
    if "oświadczam" in text:
        return "oświadczenie"
    return "inne"

def extract_requests(text):
    requests = []
    if "Wnoszę o" in text:
        parts = text.split("Wnoszę o")[-1]
        lines = parts.split("\n")
        for l in lines:
            l = l.strip()
            if l and l[0].isdigit():
                requests.append(l)
    return requests

def extract_legal(text):
    matches = re.findall(r'art\. ?\d+[a-zA-Z]*', text)
    return [{"article": m} for m in matches]

def extract_events(text):
    matches = re.findall(r'\d{2}\.\d{2}\.\d{4}', text)
    return [{"date": m} for m in matches]

def build_extraction(text):
    return {
        "document_type": classify_document(text),
        "signature": extract_signature(text),
        "facts": [],
        "events": extract_events(text),
        "requests": extract_requests(text),
        "legal_references": extract_legal(text),
        "theses": [],
        "institutional_actions": [],
        "pressure_signals": [],
        "language_assessment": {},
        "legal_assessment": {},
        "risk_analysis": {},
        "strategy": {}
    }

def main():
    with open("input.md", "r", encoding="utf-8") as f:
        text = f.read()

    extraction = build_extraction(text)

    with open("output.json", "w", encoding="utf-8") as f:
        json.dump(extraction, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    main()
