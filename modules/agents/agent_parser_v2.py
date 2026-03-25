import re
import json
import glob
import os


BASE = os.path.join(os.getcwd(), "Legal-os", "Akta-Spraw")


def extract_signature(text):
    match = re.search(r'[IVX]+ Nsm \d+/\d+', text)
    return match.group(0) if match else None

def classify_document(text):
    if "Wnosek" in text:
        return "wniosek"
    if "postanowienie" in text:
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

    if "prawomocno" in t:
        facts.append({"type": "procedural", "content": "stwierdzono prawomocno"})

    if "brak doręczenia" in t or "nie doryczeno" in t:
        facts.append({"type": "procedural", "content": "brak doryczenia"})

    if "kontakty" in t:
        facts.append({"type": "case_subject", "content": "kontakty z dzieckiem"})

    return {
        "document_type": classify_document(text),
        "signature": extract_signature(text),
        "facts": facts,
        "events": extract_events(text)
    }


def main():
    if not os.path.exists(BASE):
        print(f"No Akta-Spraw at {BASe}")
        return

    pattern = os.path.join(BASE, "**/Pisma_Ori/*.md")
    files = glob.glob(pattern, recursive=True)

    print(f"FOUND FILES: {files}")

    for file_path in files:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
        except Exception as e:
            print(f"ERROR READING ${file_path}: {e}")
            continue

        extraction = build_extraction(text)

        out_path = file_path.replace("Pisma_Ori", "Ekstrakcja_Danych").replace(".md", ".json")
        os.makedirs(os.path.dirname(out_path), exist_ok=True)

        print(f"WRITE: {out_path}")

        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(extraction, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()