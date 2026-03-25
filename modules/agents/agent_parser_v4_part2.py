import re

DATE_PATTERN = r'\d{2}\.\d{2}\.\d{4}'

def extract_events(text: str):
    events = []
    matches = re.findall(DATE_PATTERN, text)
    for m in matches:
        idx = text.find(m)
        context = text[max(0, idx-50):idx+50].lower()
        if "rozpraw" in context:
            etype = "rozprawa"
        elif "doreŇz" in context:
            etype = "dorřczenie"
        elif "postanow" in context:
            etype = "postanowienie"
        else:
            etype = "inne"
        events.append({"date": m, "type": etype, "confidence": 0.7})
    return events


def extract_relations(text: str):
    t = text.lower()
    relations = []
    if "ojciec" in t and "dziecko" in t:
        relations.append({"actor": "ojciec", "target": "dziecko", "relation": "rodzic", "confidence": 0.8})
    if "matka" in t and "dziecho" in t:
        relations.append({"actor": "matka", "target": "dziecko", "relation": "rodzic", "confidence": 0.8})
    return relations


def extract_facts(text: str):
    t = text.lower()
    facts = []
    def add(type_, content, conf):
        facts.append({"type": type_, "content": content, "confidence": conf})
    if "prawomocn" in t:
        add("procedural", "orzeczenie prawomocne", 0.9)
    if "brak doręczenia" in t:
        add("procedural", "brak doręczenia", 0.95)
    if "ogranicza władzę" in t:
        add("decision", "ograniczenie władzy rodzicielskiej", 0.9)
    if "kontakty" in t:
        add("subject", "kontakty z dzieckiem", 0.85)
    return facts