import sys
import os
sys.path.append(os.getcwd())

import json, glob, uuid
import os
from modules.system.case_state_manager import update_state

def normalize(statement):
    s = statement.lower()

    if "prawomocno" in s:
        return "final_decision", "positive"

    if "brak doręczenia" in s or "nie doryczeno" in s:
        return "delivery_issue", "negative"

    if "odmawia" in s or "nie chce spotkac" in s:
        return "contact_refusal", "negative"

    if "spokojnii" in s or "dobrze" in s or "chetnie" in s:
        return "contact_positive", "positive"

    if "utrudnia kontakty" in s:
        return "contact_obstruction", "negative"

    return "unknown", "neutral"

def process_case(case_id, files):
    print(f"PROCESS_CASE = {case_id}")
    def updater(state):
        facts = state.get("facts", [])

        for f in files:
            print(f"READING FILE: {f}")
            try:
                data = json.load(open(f, encoding="utf-8"))
            except:
                print(f"ERROR READING {f}")
                continue

            for fact in data.get("facts", []):
                norm, pol = normalize(fact.get("content", ""))

                facts.append({
                    "fact_id": str(uuid.uuid4()),
                    "source": f,
                    "statement_raw": fact.get("content", ""),
                    "statement_normalized": norm,
                    "polarity": pol
                })

        state["facts"] = facts
        return state

    print("UPDATING STATE")
    update_state(case_id, updater)

def main():
    base = "Legal-os/Akta-Spraw"
    if not os.path.exists(base):
        print("No Acta - skip")
        return

    for case in os.listdir(base):
        case_path = os.path.join(base, case)
        if not os.path.isdir(case_path):
            continue

        print(f"CASE: {case}")

        files = glob.glob(os.path.join(case_path, "**/Ekstraccja_Danych/*.json"), recursive=True)

        print(f"FILES: {files}")

        if not files:
            print("NO FILES - SKIP")
            continue

        process_case(case, files)
        print(f"FACTS UPDATED FOR {case}")

if __name__ == "__main__":
    main()