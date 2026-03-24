
import json

HEADER = "Działając wspólnie jako rodzice małoletniego Dawida Adamowicza,"

def build_response(intel):
    lines = []

    if intel.get("contradictions", 0) > 0:
        lines.append("Stanowisko strony przeciwnej pozostaje wewnętrznie niespójne i nie może stanowić podstawy do dokonania prawidłowych ustaleń faktycznych.")

    if "final_decision" in intel.get("facts_detected", []):
        lines.append("Fakt powoływania się na prawomocność rozstrzygnięcia nie eliminuje konieczności oceny prawidłowości postępowania, które do niego doprowadziło.")

    lines.append("Działania wnioskodawczyni mają charakter eskalacyjny i destabilizujący, prowadząc do zwiększenia napięcia w otoczeniu małoletniego.")

    lines.append("Brak jest podstaw do przyjęcia, iż ingerencja instytucjonalna była konieczna i proporcjonalna.")

    return lines


def main():
    try:
        intel = json.load(open("case_intelligence.json"))
    except:
        intel = {}

    response = build_response(intel)

    document = HEADER + "\n\nODPOWIEDŹ NA STANOWISKO STRONY PRZECIWNEJ\n\n" + "\n".join(["- " + r for r in response])

    with open("counter_attack.md", "w", encoding="utf-8") as f:
        f.write(document)


if __name__ == "__main__":
    main()
