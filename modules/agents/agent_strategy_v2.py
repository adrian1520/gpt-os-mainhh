# agent_strategy_v2.py

import json

def detect_phase(risk):
    risks = risk.get("risk_analysis", {}).get("risks", [])
    for r in risks:
        if r.get("type") == "procedural" and r.get("severity") == "critical":
            return "defense"
    return "monitoring"

def build_strategy(extraction, risk):
    phase = detect_phase(risk)

    priorities = []
    recommended = []
    forbidden = []
    rules = []
    outcomes = []

    risks = risk.get("risk_analysis", {}).get("risks", [])

    for r in risks:
        if r.get("type") == "procedural":
            priorities.append({
                "action": "podnieść zarzut braku doręczenia",
                "priority": "critical",
                "reason": "naruszenie prawa do obrony"
            })
            priorities.append({
                "action": "wniosek o wstrzymanie wykonania",
                "priority": "critical"
            })
            outcomes.append("możliwość uchylenia skutków")

        if r.get("type") == "institutional":
            recommended.append("utrzymać komunikację formalną")
            forbidden.append("eskalacja emocjonalna")

    rules += [
        "komunikacja neutralna",
        "dokumentowanie wszystkich zdarzeń",
        "argumentacja oparta o dobro dziecka"
    ]

    return {
        "strategy": {
            "phase": phase,
            "main_goal": "ochrona pozycji procesowej",
            "priorities": priorities,
            "recommended_actions": recommended,
            "forbidden_actions": forbidden,
            "tactical_rules": rules,
            "expected_outcomes": outcomes
        }
    }

def main():
    with open("output.json","r",encoding="utf-8") as f:
        extraction = json.load(f)

    with open("risk.json","r",encoding="utf-8") as f:
        risk = json.load(f)

    strategy = build_strategy(extraction, risk)

    with open("strategy.json","w",encoding="utf-8") as f:
        json.dump(strategy,f,indent=2,ensure_ascii=False)

if __name__ == "__main__":
    main()
