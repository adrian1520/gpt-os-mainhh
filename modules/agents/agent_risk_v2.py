# agent_risk_v2.py

import json

import glob

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
            "evidence": [text_facts],
            "impact": "naruszenie prawa do obrony"
        })
    return risks

def build_risk_for_all(extractions):
    all_risks = []

    for extraction in extractions:
        all_risks += detect_procedural_risk(extraction)

    global_risk = "low"
    if any(r["severity"] == "critical" for r in all_risks):
        global_risk = "high"
    elif any(r["severity"] == "high" for r in all_risks):
        global_risk = "medium"

    return {
        "risk_analysis": {
            "global_risk": global_risk,
            "risks": all_risks
        }
    }

def load_extractions():
    files = glob.glob("Legal-os/Akta-Spraw/**/Ekstrakcja_Danych/*.json", recursive=True)
    data = []

    for fpath in files:
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                data.append(json.load(f))
        except:
            continue

    return data

def main():
    extractions = load_extractions()

    if not extractions:
        print("No extraction files found")
        return

    risk = build_risk_for_all(extractions)

    with open("risk.json","w",encoding="utf-8") as f:
        json.dump(risk,f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    main()
