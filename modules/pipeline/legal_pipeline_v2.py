# LEGAL PIPELINE V2 (ML INFERENCE ENABLED)

import json
import os
import pickle
from datetime import datetime

from modules.agents.agent_parser_v4 import parse
from modules.agents.agent_fact_engine import extract_facts
from modules.agents.agent_law_match import match_law
from modules.agents.agent_risk_analysis import analyze_risk
from modules.agents.agent_strategy_v2 import build_strategy
from modules.agents.agent_aggregator import aggregate_output

MEMORY_PATH = "memory/learning_log.json"
FEEDBACK_PATH = "memory/feedback.json"
MODEL_PATH = "models/model.pkl"


def load_json(path):
    if not os.path.exists(path):
        return []
    with open(path, "r") as f:
        return json.load(f)


def load_model():
    if not os.path.exists(MODEL_PATH):
        return None
    with open(MODEL_PATH, "rb") as f:
        return pickle.load(f)


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


def ml_predict(model, score, risk):
    if not model:
        return None
    risk_val = 1 if "high" in str(risk).lower() else 0
    prob = model.predict_proba([[score, risk_val]])[0][1]
    return prob


def decision_from_ml(prob, strategy):
    if prob is None:
        return None

    if prob >= 0.75:
        action = "strong_proceed"
    elif prob >= 0.6:
        action = "proceed"
    elif prob >= 0.4:
        action = "proceed_with_caution"
    else:
        action = "do_not_proceed"

    return {
        "action": action,
        "confidence": round(prob, 2),
        "recommended_strategy": strategy
    }


def run_pipeline(input_data):
    history = load_json(MEMORY_PATH)
    history = merge_feedback(history)
    model = load_model()

    parsed = parse(input_data)
    facts = extract_facts(parsed)
    law = match_law(facts)
    risk = analyze_risk(facts, law)
    strategy = build_strategy(facts, law, risk)
    output = aggregate_output(strategy)

    base_score = 50
    prob = ml_predict(model, base_score, risk)
    decision = decision_from_ml(prob, strategy)

    if decision is None:
        decision = {"action": "fallback", "confidence": 0.5}

    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "risk": str(risk),
        "score": base_score,
        "outcome": "unknown"
    }

    save_memory(entry)

    return {
        "facts": facts,
        "law": law,
        "risk": risk,
        "strategy": strategy,
        "output": output,
        "ml_probability": prob,
        "decision": decision,
        "ml_enabled": model is not None
    }
