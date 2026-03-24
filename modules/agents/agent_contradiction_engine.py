
import json, itertools, uuid

def main():
    facts = json.load(open("facts.json",encoding="utf-8"))
    contradictions = []

    for a,b in itertools.combinations(facts,2):
        if a["statement_normalized"] == b["statement_normalized"]:
            continue
        if a["polarity"] != b["polarity"]:
            contradictions.append({
                "id": str(uuid.uuid4()),
                "fact_A": a["fact_id"],
                "fact_B": b["fact_id"],
                "type": "statement_conflict"
            })

    json.dump(contradictions, open("contradictions.json","w",encoding="utf-8"), indent=2, ensure_ascii=False)

if __name__ == "__main__":
    main()
