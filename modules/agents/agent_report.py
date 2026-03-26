import json


def build_report(reasoning_output):
    report = {}

    report["tags"] = reasoning_output.get("tags", [])
    report["evidence"] = reasoning_output.get("evidence", {})
    report["contradictions"] = reasoning_output.get("contradictions", [])
    report["strategy"] = reasoning_output.get("strategy", [])
    report["arguments"] = reasoning_output.get("arguments", [])
    report["multi_scenario"] = reasoning_output.get("multi_scenario", [])
    report["judge_scenario"] = reasoning_output.get("judge_scenario", [])

    score = reasoning_output.get("evidence", {}).get("score", 0)

    if score > 7:
        report["assessment"] = "strong"
    elif score > 3:
        report["assessment"] = "medium"
    else:
        report["assessment"] = "weak"
    
    return report
