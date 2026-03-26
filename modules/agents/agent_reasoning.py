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
    for f in facts:
        txt = f.get("content", "").lower()
        if "dowod" in txt:
            score += 2
        if "zeznania" in txt:
            score += 1
    return score


def simulate_judge(tags, evidence_score):
    profiles = []

    # Restrictive judge
    profiles.append({
        "name": "restrictive",
        "bias": "wysokia ochrona dziecka",
        "outcome": "Chetnie ogranicza władze przy ryzyku",
        "probability": 0.7 - (evidence_score / 10)
    })

    # Balanced judge
    profiles.append({
        "name": "balanced",
        "bias": "analiza dowodów",
        "outcome": "Decyzja woparta na dowodach",
        "probability": 0.6 + (evidence_score / 10)
    })

    # Lenient judge
    profiles.append({
        "name": "lenient",
        "bias": "ochrona relacji rodzinnych",
        "outcome": "Forytze kontakty i młniejsze intervencje",
        "probability": 0.5 + (evidence_score / 10)
    })

    return profiles


def build_reasoning(data):
    output = {
        "tags": [],
        "evidence": 0,
        "judge_scenario": []
    }

    facts = data.get("facts", [])

    tags = detect_tags(facts)
    output["tags"] = tags

    evidence_score = score_evidence(facts)
    output["evidence"] = evidence_score

    output["judge_scenario"] = simulate_judge(tags, evidence_score)

    return output
