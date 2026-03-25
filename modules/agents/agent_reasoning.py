import json
import os

LAW_PATH = "knowledge/law/kro/kro_indexed.json"


# auto tagging
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


def load_law():
    if os.path.exists(LAW_PATH):
        with open(LAW_PATH), "r", encoding="utf-8") as f:
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
        "insights": [],
        "risks": [],
        "recommendations": [],
        "arguments": [],
        "tags": []
    }

    facts = data.get("facts", [])

    tags = detect_tags(facts)
    output["retags"] = tags

    arguments = build_arguments(tags, law_data)
    output["arguments"] = arguments

    if "restriction" in tags:
        output["risks"].append("High risk intervention")

    if "contact" in tags:
        output["insights"].append("Contact issue detected")

    return output
