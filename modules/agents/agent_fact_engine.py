
import json, glob, uuid

def normalize(statement):
    s = statement.lower()
    if "odmawia" in s or "nie chce" in s:
        return "contact_refusal","negative"
    if "spokojnie" in s or "dobrze" in s:
        return "contact_positive","positive"
    if "brak doręczenia" in s:
        return "delivery_issue","negative"
    return "unknown","neutral"

def main():
    files = glob.glob("Legal-os/Akta-Spraw/**/Ekstrakcja_Danych/*.json", recursive=True)
    facts = []

    for f in files:
        data = json.load(open(f,encoding="utf-8"))
        for fact in data.get("facts",[]):
            norm, pol = normalize(fact.get("content",""))
            facts.append({
                "fact_id": str(uuid.uuid4()),
                "source": f,
                "statement_raw": fact.get("content",""),
                "statement_normalized": norm,
                "polarity": pol
            })

    json.dump(facts, open("facts.json","w",encoding="utf-8"), indent=2, ensure_ascii=False)

if __name__ == "__main__":
    main()
