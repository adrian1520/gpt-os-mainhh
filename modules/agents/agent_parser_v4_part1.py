import re

SIGNATURE_PATTERNS = [
    (r'[IVX]+\s*Nsm\s*\d+/\d+', 0.95),
    (r'[IVX]+\s*Ns\s*\d+/\d+', 0.9),
]

def normalize(text: str):
    return text.lower().strip()

def extract_signature(text: str):
    for pattern, conf in SIGNATURE_PATTERNS:
        m = re.search(pattern, text, re.IGNORECASE)
        if m:
            return {"value": m.group(0), "confidence": conf}
    return {"value": None, "confidence": 0.0}


def classify_document(text: str):
    t = normalize(text)
    if "wniosek" in t:
        return {"value": "wniosek", "confidence": 0.95}
    if "postamowienie" in t:
        return {"value": "postanowienie", "confidence": 0.95}
    return {"value": "inne", "confidence": 0.5}
