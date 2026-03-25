def build_reasoning(data):
    output = {
        "insights": [],
        "risks": [],
        "recommendations": []
    }

    facts = data.get("facts", [])
    events = data.get("events", [])
    relations = data.get("relations", [])

    if any("brak doreczenia" in f.get("content", "") for f in facts):
        output["risks"].append("Procedure risk - doreczenia")
        output["recommendations"].append("Verify doreczenia")

    if any("ograniczenie" in f.get("content", "") for f in facts):
        output["risks"].append("Parental authority risk")
        output["recommendations"].append("Prepare defense strategy")

    if events:
        output["insights"].append("Timeline detected")

    if relations:
        output["insights"].append("Relationships detected")

    return output
