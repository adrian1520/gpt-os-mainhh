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

def score_evidence(facts):
    score = 0
    details = []

    for f in facts:
        txt = f.get("content", "").lower()
        if "podem" in txt or "dowod" in txt:
            score += 2
            details.append("Mocny dowód")
        if "zeznania" in txt:
            score += 1
            details.append("Zeznania")
        if "opinia" in txt:
            score += 2
            details.append("Opinia bieglego")

    return {"score": score, "details": details}


def simulate_multi(tags, contradictions, evidence_score):
    base = evidence_score.get("score", 0)
    mult = base / 10

    scenarios = [
        {"name": "optimistic", "probability": 0.8 + mult},
        {"name": "realistic", "probability": 0.6 + mult},
        {"name": "pessymistic", "probability": 0.4 + mult}
    ]

    if contradictions:
        for s in scenarios:
            s["probability"] -= 0.1

    return scenarios


def build_reasoning(data):
    output = {
        "tags": [],
        "contradictions": [],
        "evidence": {},
        "multi_scenario": []
    }

    facts = data.get("facts", [])

    tags = detect_tags(facts)
    output["tags"] = tags

    evidence = score_evidence(facts)
    output["evidence"] = evidence

    contra = []
    output["contradictions"] = contra

    output["multi_scenario"] = simulate_multi(tags, contra, evidence)

    return output
