
import re
import json
import glob
import os

def extract_signature(text):
    match = re.search(r'[IVX]+ Nsm \d+/\d+', text)
    return match.group(0) if match else None

def classify_document(text):
    if "Wnoszę" in text:
        return "wniosek"
    if "postanowienia" in text:
        return "postanowienie"
    if "wzywa" in text:
        return "wezwanie"
    return "inne"

def extract_events(text):
    matches = re.findall(r'\d{2}\.\d{2}\.\d{4}', text)
    return [{"date": m} for m in matches]

def build_extraction(text):
    facts = []
    t = text.lower()

    if "prawomocność" in t:
        facts.append({"type": "procedural", "content": "stwierdzono prawomocność"})

    if "brak doręczenia" in t or "nie doręczono" in t:
        facts.append({"type": "procedural", "content": "brak doręczenia"})

    if "kontakty" in t:
        facts.append({"type": "case_subject", "content": "kontakty z dzieckiem"})

    return {
        "document_type": classify_document(text),
        "signature": extract_signature(text),
        "facts": facts,
        "events": extract_events(text)
    }

def main():
    files = glob.glob("Legal-os/Akta-Spraw/**/Pisma_Ori/*.md", recursive=True)

    for file_path in files:
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()

        extraction = build_extraction(text)

        out_path = file_path.replace("Pisma_Ori", "Ekstrakcja_Danych").replace(".md", ".json")
        os.makedirs(os.path.dirname(out_path), exist_ok=True)

        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(extraction, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    main()
