import re
import json
import glob
import os
from datetime import datetime

BASE = "Legal-os/Akta-Spraw"


def normalize(text: str) -> str:
    return text.lower().strip()


SIGNATURE_PATTERNS = [
    r'[IVX]+\s*Nsm\s*\d+/\d+',
    r'[IVX]+\s*Ns\s*\d+/\d+',
    r'[A-Z]+\s*\d+/\d+',
]

def extract_signature(text: str):
    for pattern in SIGNATURE_PATTERNS:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(0)
    return None


def classify_document(text: str):
    t = normalize(text)

    if "wniosek" in t:
        return "wniosek"
    if "postanowienie" in t:
        return "postanowienie"
    if "wezwanie" in t or "wzywa" in t:
        return "wezwanie"
    if "zarządzenie" in t:
        return "zarządzenie"

    return "inne"


DATE_PATTERNS = [
    r'\d{2}\.\d{2}\.\d{4}',
    r'\d{4}-\d{2}-\d{2}',
]

def extract_dates(text: str):
    dates = set()

    for pattern in DATE_PATTERNS:
        matches = re.findall(pattern, text)
        for m in matches:
            dates.add(m)

    return [{"date": d} for d in sorted(dates)]


def extract_entities(text: str):
    t = normalize(text)

    entities = []

    if "matka" in t:
        entities.append({"role": "matka"})
    if "ojciec" in t:
        entities.append({"role": "ojciec"})
    if "dziecko" in t:
        entities.append({"role": "dziecko"})

    return entities


def extract_facts(text: str):
    t = normalize(text)
    facts = []

    def add(type_, content):
        facts.append({
            "type": type_,
            "content": content
        })

    if "prawomocn" in t:
        add("procedural", "orzeczenie prawomocne")

    if "brak doręczenia" in t or "nie doręczono" in t:
        add("procedural", "brak doręczenia")

    if "kontakty" in t:
        add("case_subject", "kontakty z dzieckiem")

    if "ogranicza władzę" in t:
        add("decision", "ograniczenie władzy rodzicielskiej")

    if "zakazuje" in t:
        add("decision", "zakaz")

    return facts


def validate_extraction(data: dict):
    if not data.get("document_type"):
        data["document_type"] = "unknown"

    if not isinstance(data.get("facts"), list):
        data["facts"] = []

    if not isinstance(data.get("events"), list):
        data["events"] = []

    return data


def build_extraction(text: str):
    extraction = {
        "document_type": classify_document(text),
        "signature": extract_signature(text),
        "entities": extract_entities(text),
        "facts": extract_facts(text),
        "events": extract_dates(text),
    }

    return validate_extraction(extraction)


def process_file(file_path: str):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
    except Exception as e:
        print(f"ERROR reading {file_path}: {e}")
        return

    extraction = build_extraction(text)

    out_path = (
        file_path
        .replace("Pisma_Ori", "Ekstrakcja_Danych")
        .replace(".md", ".json")
    )

    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(extraction, f, indent=2, ensure_ascii=False)

    print(f"WRITE: {out_path}")


def main():
    if not os.path.exists(BASE):
        print(f"Missing path: {BASE}")
        return

    pattern = os.path.join(BASE, "**/Pisma_Ori/*.md")
    files = glob.glob(pattern, recursive=True)

    print(f"FOUND FILES: {len(files)}")

    for file_path in files:
        process_file(file_path)


if __name__ == "__main__":
    main()