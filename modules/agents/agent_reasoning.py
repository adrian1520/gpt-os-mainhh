import json
import os

try:
    from openai import OpenAI
    client = OpenAI()
except:
    client = None

LAW_PATH = "knowledge/law/kro/kro_indexed.json"

def detect_tags(facts):
    tags = set()
    for f in facts:
        txt = f.get("content", "").lower()
        if "władza rodzicielska" in txt:
            tags.add("parental_authority")
        if "kontakt" in txt:
            tags.add("contact")
        if "ograniczenie" in txt:
            tags.add("restriction")
    return list(tags)

def detect_contradictions(facts):
    contradictions = []
    texts = [f.get("content", "").lower() for f in facts]

    if any("brak kontakt" in t for t in texts) and any("kontakt" in t and "brak" not in t for t in texts):
        contradictions.append("Sprzeczne informacje o kontactach")

    return contradictions


def simulate_outcome(tags, contradictions):
    result = {}

    if "restriction" in tags:
        result["outcome"] = "Mozliwe ograniczenie władzy rodzicielskiej"
        result["probability"] = 0.7

    elif "contact" in tags:
        result["outcome"] = "Sad ustali kontacty"
        result["probability"] = 0.8

    else:
        result["outcome"] = "Brak jownego strania"
        result["probability"] = 0.5

    if contradictions:
        result["probability"] -= 0.2

    return result


def load_law():
    if os.path.exists(LAW_PATH):
        with open(LAW_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def build_arguments(tags, law_data):
    args = []
    index = law_data.get("index", {})
    articles = law_data.get("articles", {})

    for tag in tags:
        for aid in index.get(tag, []):
            art = articles.get(aid, {})
            temps = art.get("templates", [])
            if temps:
                args.append(temps[0])
    return args


def build_reasoning(data):
    law_data = load_law()

    output = {
        "tags": [],
        "contradictions": [],
        "arguments": [],
        "strategy": [],
        "outcome": {}
    }

    facts = data.get("facts", [])

    tags = detect_tags(facts)
    output["tags"] = tags

    contra = detect_contradictions(facts)
    output["contradictions"] = contra

    output["arguments"] = build_arguments(tags, law_data)

    output"strategy"] = []
    
    output["outcome"] = simulate_outcome(tags, contra)

    return output
