# LEGAL PIPELINE V2 (REAL FEEDBACK INTEGRATION)

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
FEEDBACK_PATH = "memory/feedback.json"


def load_json(path):
    if not os.path.exists(path):
        return []
    with open(path, "r") as f:
        return json.load(f)


def save_memory(entry):
    data = load_json(MEMORY_PATH)
    data.append(entry)
    with open(MEMORY_PATH, "w") as f:
        json.dump(data, f, indent=2)


def merge_feedback(history):
    feedback = load_json(FEEDBACK_PATH)
    feedback_map = {f.get("timestamp"): f for f in feedback}

    for h in history:
        ts = h.get("timestamp")
        if ts in feedback_map:
            h["outcome"] = feedback_map[ts].get("outcome", h.get("outcome"))

    return history


def weighted_average(history):
    if not history:
        return 50
    total, weight_sum = 0, 0
    for i, h in enumerate(reversed(history[-30:])):
        w = i + 1
        total += h.get("score", 50) * w
        weight_sum += w
    return total / weight_sum if weight_sum else 50


def reinforcement_adjustment(history):
    reward, count = 0, 0
    for h in history[-20:]:
        if h.get("outcome") == "win":
            reward += 10
            count += 1
        elif h.get("outcome") == "loss":
            reward -= 10
            count += 1
    return (reward / count) if count else 0


def scoring_engine(risk, facts, history):
    score = 50
    r = str(risk).lower()

    if "high" in r:
        score -= 30
    elif "low" in r:
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
    history = load_json(MEMORY_PATH)
    history = merge_feedback(history)

    parsed = parse(input_data)
    facts = extract_facts(parsed)
    law = match_law(facts)
    risk = analyze_risk(facts, law)
    strategy = build_strategy(facts, law, risk)
    output = aggregate_output(strategy)

    score = scoring_engine(risk, facts, history)
    decision = decision_engine(strategy, score)

    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "risk": str(risk),
        "score": score,
        "outcome": "unknown"
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
        "feedback_integrated": True
    }
