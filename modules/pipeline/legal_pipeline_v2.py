# LEGAL PIPELINE V2 (DECISION ENGINE + SCORING)

from modules.agents.agent_parser_v4 import parse
from modules.agents.agent_fact_engine import extract_facts
from modules.agents.agent_law_match import match_law
from modules.agents.agent_risk_analysis import analyze_risk
from modules.agents.agent_strategy_v2 import build_strategy
from modules.agents.agent_aggregator import aggregate_output


def scoring_engine(risk, facts):
    score = 50

    risk_str = str(risk).lower()

    if "high" in risk_str:
        score -= 30
    elif "low" in risk_str:
        score += 20

    if facts:
        score += 10

    return max(0, min(100, score))


def decision_engine(risk, strategy, score):
    decision = {}

    if score >= 70:
        decision["action"] = "strong_proceed"
    elif score >= 40:
        decision["action"] = "proceed_with_caution"
    else:
        decision["action"] = "do_not_proceed"

    decision["score"] = score
    decision["confidence"] = round(score / 100, 2)
    decision["recommended_strategy"] = strategy

    return decision


def run_pipeline(input_data):
    parsed = parse(input_data)

    facts = extract_facts(parsed)

    law = match_law(facts)

    risk = analyze_risk(facts, law)

    strategy = build_strategy(facts, law, risk)

    output = aggregate_output(strategy)

    score = scoring_engine(risk, facts)

    decision = decision_engine(risk, strategy, score)

    return {
        "facts": facts,
        "law": law,
        "risk": risk,
        "strategy": strategy,
        "output": output,
        "score": score,
        "decision": decision
    }
