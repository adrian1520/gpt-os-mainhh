# LEGAL PIPELINE V2 (DETERMINISTIC + DECISION ENGINE)

from modules.agents.agent_parser_v4 import parse
from modules.agents.agent_fact_engine import extract_facts
from modules.agents.agent_law_match import match_law
from modules.agents.agent_risk_analysis import analyze_risk
from modules.agents.agent_strategy_v2 import build_strategy
from modules.agents.agent_aggregator import aggregate_output


def decision_engine(risk, strategy):
    decision = {}

    # simple deterministic rules (can be expanded)
    risk_level = str(risk).lower()

    if "high" in risk_level:
        decision["action"] = "proceed_with_caution"
    elif "low" in risk_level:
        decision["action"] = "proceed"
    else:
        decision["action"] = "analyze_further"

    decision["confidence"] = 0.7
    decision["recommended_strategy"] = strategy

    return decision


def run_pipeline(input_data):
    parsed = parse(input_data)

    facts = extract_facts(parsed)

    law = match_law(facts)

    risk = analyze_risk(facts, law)

    strategy = build_strategy(facts, law, risk)

    output = aggregate_output(strategy)

    decision = decision_engine(risk, strategy)

    return {
        "facts": facts,
        "law": law,
        "risk": risk,
        "strategy": strategy,
        "output": output,
        "decision": decision
    }
