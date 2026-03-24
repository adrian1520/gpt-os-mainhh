
import json

TEMPLATE_HEADER = "Działając wspólnie jako rodzice małoletniego Dawida Adamowicza,"

def tone_block():
    return "Wszelkie działania ingerujące w sferę wychowawczą dziecka muszą pozostawać w ścisłej zgodności z jego dobrem, a każda ingerencja instytucjonalna powinna mieć charakter proporcjonalny i uzasadniony."

def build_actions(intel):
    actions = []

    state = intel.get("legal_state")

    if state == "procedural_violation":
        actions.append("wnosimy o uchylenie zaskarżonego postanowienia w całości")
        actions.append("wnosimy o wstrzymanie wykonania orzeczenia")

    elif state == "final_decision_detected":
        actions.append("wnosimy o weryfikację prawidłowości procedury poprzedzającej wydanie orzeczenia")

    if intel.get("contradictions", 0) > 0:
        actions.append("wnosimy o wyjaśnienie sprzeczności w materiale dowodowym")

    if not actions:
        actions.append("wnosimy o przeprowadzenie uzupełniającego postępowania dowodowego")

    return actions


def build_justification(intel):
    parts = []
    idx = 1

    facts = intel.get("facts_detected", [])

    if "final_decision" in facts:
        parts.append(f"{idx}. Stwierdzenie prawomocności orzeczenia nakłada obowiązek szczególnie wnikliwej kontroli prawidłowości przebiegu postępowania, w szczególności w kontekście ochrony dobra małoletniego (art. 95 §1 k.r.o.).")
        idx += 1

    if intel.get("legal_state") == "procedural_violation":
        parts.append(f"{idx}. W toku postępowania doszło do uchybień o charakterze proceduralnym, które mogły mieć istotny wpływ na treść rozstrzygnięcia, co uzasadnia jego kontrolę instancyjną.")
        idx += 1

    if intel.get("contradictions", 0) > 0:
        parts.append(f"{idx}. Zgromadzony materiał dowodowy pozostaje niespójny, co uniemożliwia dokonanie prawidłowych ustaleń faktycznych bez uprzedniego wyjaśnienia rozbieżności.")
        idx += 1

    parts.append(f"{idx}. Dodatkowo wskazać należy, iż wszelkie próby ingerencji instytucjonalnej w stabilne środowisko wychowawcze dziecka, w szczególności poprzez nadmierne zaangażowanie organów zewnętrznych, stanowią nieproporcjonalną ingerencję, prowadzącą do eskalacji stresu u małoletniego.")
    idx += 1

    parts.append(f"{idx}. Nadrzędnym kryterium oceny każdej decyzji pozostaje dobro małoletniego (art. 113² §1 k.r.o.), które w niniejszej sprawie wymaga zachowania stabilności, przewidywalności oraz minimalizacji czynników destabilizujących.")

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

{tone_block()}

{justification}
"""

    with open("legal_action.md", "w", encoding="utf-8") as f:
        f.write(document)


if __name__ == "__main__":
    main()
