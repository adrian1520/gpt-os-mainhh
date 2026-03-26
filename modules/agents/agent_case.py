import json
import os
from datetime import datetime


def create_case(case_id):
    return {
        "case_id": case_id,
        "documents": [],
        "facts": [],
        "evidence": [],
        "timeline": []
    }


def add_document(case, doc_type, side, content):
    doc = {
        "type": doc_type,
        "side": side,
        "content": content,
        "date": datetime.now().isoformat()
    }

    case["documents"].append(doc)
    case["timeline"].append(doc)

    extract_from_document(case, doc)

    return case


def extract_from_document(case, doc):
    text = doc.get("content", "").lower()

    if "kontakt" in text:
        case["facts"].append({"content": "dortyczy kontaktu"})

    if "ograniczenie" in text:
        case["facts"].append({"content": "mozliwe ograniczenie władzy"})

    if "dowod" in text:
        case["evidence"].append({"content": "dowod"})


def get_case_summary(case):
    return {
        "case_id": case.get("case_id"),
        "document_count": len(case.get("documents", [])),
        "fact_count": len(case.get("facts", ([]))),
        "evidence_count": len(case.get("evidence", []))
    }
