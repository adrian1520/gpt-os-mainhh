# LEGAL PIPELINE V2 (LEARNING SYSTEM)

import json
import os

from modules.agents.agent_parser_v4 import parse
from modules.agents.agent_fact_engine import extract_facts
from modules.agents.agent_law_match import match_law
from modules.agents.agent_risk_analysis import analyze_risk
from modules.agents.agent_strategy_v2 import build_strategy
from modules.agents.agent_aggregator import aggregate_output

MEMORY_PATH = "memory/learning_log.json"


def load_memory():
    if not os.path.exists(MEMORY_PATH):
        return []
    with open(MEMORY_PATH, "r") as f:
        return json.load(f)


def save_memory(entry):
    data = load_memory()
    data.append(entry)
    with open(MEMORY_PATH, "w") as f:
        json.dump(data, f, indent=2)


def scoring_engine(risk, facts, history):
    score = 50

    risk_str = str(risk).lower()

    if "high" in risk_str:
        score -= 30
    elif "low" in risk_str:
        score += 20

    if facts:
        score += 10

    # learning influence
    if history:
        avg = sum([h.get("score", 50) for h in history]) / len(history)
        score = int((score + avg) / 2)

    return max(0, min(100, score))


def decision_engine(strategy, score):
    if score >= 70:
        action = "strong_proceed"
    elif score >= 40:
        action = "proceed_with_caution"
    else:
        action = "do_not_proceed"

    return {
        "action": action,
        "score": score,
        "confidence": round(score / 100, 2),
        "recommended_strategy": strategy
    }


def run_pipeline(input_data):
    history = load_memory()

    parsed = parse(input_data)
    facts = extract_facts(parsed)
    law = match_law(facts)
    risk = analyze_risk(facts, law)
    strategy = build_strategy(facts, law, risk)
    output = aggregate_output(strategy)

    score = scoring_engine(risk, facts, history)
    decision = decision_engine(strategy, score)

    entry = {
        "risk": str(risk),
        "score": score
    }

    save_memory(entry)

    return {
        "facts": facts,
        "law": law,
        "risk": risk,
        "strategy": strategy,
        "output": output,
        "score": score,
        "decision": decision
    }
