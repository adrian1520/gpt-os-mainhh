# agent_risk_v2.py

import json

def detect_procedural_risk(extraction):
    risks = []
    text_facts = " ".join([f.get("content","") for f in extraction.get("facts",[])])

    if "brak doręczenia" in text_facts or "brak wezwania" in text_facts:
        risks.append({
            "type": "procedural",
            "subtype": "service_failure",
            "severity": "critical",
            "severity_score": 5,
            "confidence": 0.9,
            "evidence": ["brak doręczenia / wezwania"],
            "impact": "naruszenie prawa do obrony"
        })
    return risks

def detect_institutional_risk(extraction):
    risks = []
    if extraction.get("pressure_signals"):
        risks.append({
            "type": "institutional",
            "subtype": "pressure",
            "severity": "high",
            "severity_score": 4,
            "confidence": 0.8,
            "evidence": ["presja instytucji"]
        })
    return risks

def build_risk(extraction):
    risks = []
    risks += detect_procedural_risk(extraction)
    risks += detect_institutional_risk(extraction)

    global_risk = "low"
    if any(r["severity"] == "critical" for r in risks):
        global_risk = "high"
    elif any(r["severity"] == "high" for r in risks):
        global_risk = "medium"

    return {
        "risk_analysis": {
            "global_risk": global_risk,
            "risks": risks
        }
    }

def main():
    with open("output.json","r",encoding="utf-8") as f:
        extraction = json.load(f)

    risk = build_risk(extraction)

    with open("risk.json","w",encoding="utf-8") as f:
        json.dump(risk,f,indent=2,ensure_ascii=False)

if __name__ == "__main__":
    main()
