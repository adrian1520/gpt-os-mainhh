from modules.system.register_case import register_case
from modules.agents.agent_parser_v4 import build_extraction
from modules.agents.agent_reasoning import main as reasoning_main
from modules.agents.agent_risk_v2 import main as risk_main
from modules.agents.agent_strategy_v2 import main as strategy_main
from modules.agents.agent_legal_action import main as legal_main
from modules.agents.agent_aggregator import main as aggregator_main

def run_pipeline():
    print("PIPELINE START")

    # 1. Register
    register_case()

    # 2. Input
    try:
        with open("Legal-os/input/postanowienie_nadzor_III_Nsm_756_25.txt", "r") as f:
            text = f.read()
    except Exception as e:
        print(f"INPUT ERROR: {e}")
        text = ""

    # 3. Parse
    extraction = build_extraction(text)
    print("PARSER DONE")

    # 4. Reasoning
    reasoning_main()
    print("REASONING DONE")

    # 5. Risk
    risk_main()
    print("RISK DONE")

    # 6. Strategy
    strategy_main()
    print("STRATEGY DONE")

    # 7. Legal action
    legal_main()
    print("LEGAL ACTION DONE")

    # 8. Aggregate
    aggregator_main()
    print("AGGREGATION DONE")

    print("PIPELINE END")

if __name__ == "__main__":
    run_pipeline()
