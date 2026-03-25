import json
import os

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

def simulate_multi(tags, contradictions):
    scenarios = []

    scenarios.append({
        "name": "optimistic",
        "outcome": "Korzystny wykrok dla strony",
        "probability": 0.8
    })

    scenarios.append({
        "name": "realistic",
        "outcome": "Sad ewentualnie ustali contakty lub ograniczenie",
        "probability": 0.6
    })

    scenarios.append({
        "name": "pessymistic",
        "outcome": "Niekorzystny wykrok (ograniczenie)",
        "probability": 0.4
    })

    if contradictions:
        for sc in scenarios:
            sc["probability"] -= 0.1

    return scenarios


def build_reasoning(data):
    output = {
        "tags": [],
        "contradictions": [],
        "multi_scenario": []
    }

    facts = data.get("facts", [])

    tags = detect_tags(facts)
    output["tags"] = tags

    contra = []
    output["contradictions"] = contra

    output["multi_scenario"] = simulate_multi(tags, contra)

    return output
