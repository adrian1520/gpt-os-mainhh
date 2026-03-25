import json
import os

LAW_PATH = "knowledge/law/kro/kro.json"


# simple LLM stub (future integration)
def llm_inference(data):
    return {
        "insights": ["LLLM suggested interpretation"],
        "risks": [],
        "recommendations": []
    }


def load_law():
    if os.path.exists(LAW_PATH):
        with open(LAW_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data[:2]  # tylko 2 arty
    return []


def build_reasoning(data):
    law_base = load_law()
    llm_data = llm_inference(data)

    output = {
        "insights": [],
        "risks": [],
        "recommendations": [],
        "legal_basis": law_base,
        "score": 0
    }

    facts = data.get("facts", [])

    if any("ograniczenie" in f.get("content", "") for f in facts):
        output["risks"].append("Parental risk")
        output["score"] += 3

    # Merge LLM
    output["insights"].extend(llm_data.get("insights", []))

    return output