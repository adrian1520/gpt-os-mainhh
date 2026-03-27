# LEGAL PIPELINE V2 (DETERMINISTIC)

from modules.agents.agent_parser_v4 import parse
from modules.agents.agent_fact_engine import extract_facts
from modules.agents.agent_law_match import match_law
from modules.agents.agent_risk_analysis import analyze_risk
from modules.agents.agent_strategy_v2 import build_strategy
from modules.agents.agent_aggregator import aggregate_output


def run_pipeline(input_data):
    parsed = parse(input_data)

    facts = extract_facts(parsed)

    law = match_law(facts)

    risk = analyze_risk(facts, law)

    strategy = build_strategy(facts, law, risk)

    output = aggregate_output(strategy)

    return output
