import json


def generate_document(report):
    doc = {}

    tags = report.get("tags", [])
    arguments = report.get("arguments", [])
    strategy = report.get("strategy", [])
    evidence = report.get("evidence", {})
    contra = report.get("contradictions", [])

    doc["title"] = "Wniosek o uregulowanie situacji rodzinnej"

    doc["motion"] = []

    if "contact" in tags:
        doc["motion"].append("Ustalienie kontactów z dzieckiem")

    if "restriction" in tags:
        doc["motion"].append("Ograniczenie władzy rodzicielskiej")

    doc["arguments"] = arguments

    doc["evidence"] = evidence

    doc["strategy"] = strategy

    if contra:
        doc["extra"] = "Sprzecznosci w stanowisku przeciwnika"

    return doc
