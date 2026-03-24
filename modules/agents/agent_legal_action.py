
import json

TEMPLATE_HEADER = "Działając wspólnie jako rodzice małoletniego Dawida Adamowicza,"

def build_actions(intel):
    actions = []

    if intel.get("legal_state") == "procedural_violation":
        actions.append("wnosimy o uchylenie zaskarżonego postanowienia")

    if intel.get("legal_state") == "final_decision_detected":
        actions.append("wnosimy o weryfikację prawidłowości procedury poprzedzającej wydanie orzeczenia")

    if intel.get("contradictions", 0) > 0:
        actions.append("wnosimy o wyjaśnienie rozbieżności w materiale dowodowym")

    if not actions:
        actions.append("wnosimy o przeprowadzenie dalszego postępowania dowodowego")

    return actions


def build_justification(intel):
    parts = []

    if "final_decision" in intel.get("facts_detected", []):
        parts.append("1. W sprawie doszło do stwierdzenia prawomocności orzeczenia, co wymaga szczególnej weryfikacji pod kątem zgodności z dobrem małoletniego (art. 95 §1 k.r.o.).")

    if intel.get("legal_state") == "procedural_violation":
        parts.append("2. Wystąpiły istotne uchybienia proceduralne, które mogły mieć wpływ na wynik sprawy.")

    if intel.get("contradictions", 0) > 0:
        parts.append("3. Materiał dowodowy zawiera sprzeczności, które wymagają wyjaśnienia przed podjęciem dalszych decyzji.")

    parts.append("4. Wszelkie rozstrzygnięcia powinny być podporządkowane nadrzędnej zasadzie dobra małoletniego (art. 113² §1 k.r.o.).")

    return "\n".join(parts)


def main():
    try:
        intel = json.load(open("case_intelligence.json"))
    except:
        intel = {}

    actions = build_actions(intel)
    justification = build_justification(intel)

    document = f"""{TEMPLATE_HEADER}

Wnosimy o:
- """ + "\n- ".join(actions) + f"""

UZASADNIENIE

{justification}
"""

    with open("legal_action.md", "w", encoding="utf-8") as f:
        f.write(document)


if __name__ == "__main__":
    main()
