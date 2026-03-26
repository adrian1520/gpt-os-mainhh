import json

from modules.agents.agent_case import create_case, add_document
from modules.agents.agent_reasoning import build_reasoning
from modules.agents.agent_report import build_report
from modules.agents.agent_document import generate_document


# End-to-end pipeline
def run_case_pipeline(case_id, documents):
    case = create_case(case_id)

    # add documents
    for d in documents:
        case = add_document(
            case,
            d.get("type"),
            d.get("side"),
            d.get("content")
        )

    # reasoning input
    data = {
        "facts": case.get("facts", [])
    }

    # run engines
    reasoning = build_reasoning(data)
    report = build_report(reasoning)
    document = generate_document(report)

    return {
        "case": case,
        "reasoning": reasoning,
        "report": report,
        "document": document
    }