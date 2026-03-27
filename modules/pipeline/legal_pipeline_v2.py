# LEGAL PIPELINE V2 (AUTONOMOUS LOOP SYSTEM)

import json
import os
from datetime import datetime

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


def weighted_average(history):
    if not history:
        return 50
    total = 0
    weight_sum = 0
    for i, h in enumerate(reversed(history[-30:])):
        weight = i + 1
        total += h.get("score", 50) * weight
        weight_sum += weight
    return total / weight_sum if weight_sum else 50


def reinforcement_adjustment(history):
    if not history:
        return 0
    reward = 0
    count = 0
    for h in history[-20:]:
        if h.get("outcome") == "win":
            reward += 10
            count += 1
        elif h.get("outcome") == "loss":
            reward -= 10
            count += 1
    return (reward / count) if count else 0


def infer_outcome(score, decision):
    # autonomous outcome estimation
    if decision["action"] == "strong_proceed" and score >= 75:
        return "win"
    elif decision["action"] == "do_not_proceed":
        return "loss"
    return "unknown"


def scoring_engine(risk, facts, history):
    score = 50
    risk_str = str(risk).lower()

    if "high" in risk_str:
        score -= 30
    elif "low" in risk_str:
        score += 20

    if facts:
        score += 10

    learned = weighted_average(history)
    reinforcement = reinforcement_adjustment(history)

    score = int((score * 0.5) + (learned * 0.3) + (reinforcement * 0.2))
    return max(0, min(100, score))


def decision_engine(strategy, score):
    if score >= 80:
        action = "strong_proceed"
    elif score >= 60:
        action = "proceed"
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

    outcome = infer_outcome(score, decision)

    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "risk": str(risk),
        "score": score,
        "outcome": outcome
    }

    save_memory(entry)

    return {
        "facts": facts,
        "law": law,
        "risk": risk,
        "strategy": strategy,
        "output": output,
        "score": score,
        "decision": decision,
        "autonomous_outcome": outcome
    }
