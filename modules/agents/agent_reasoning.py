import json
import os

try:
    from openai import OpenAI
    client = OpenAI()
except:
    client = None

LAW_PATH = "knowledge/law/kro/kro_indexed.json"

def detect_tags(facts):
    tags = set()
    for f in facts:
        txt = f.get("content", "").lower()
        if "władza rodzicielska" in txt:
            tags.add("parental_authority")
        if "kontakt" in txt:
            tags.add("contact")
        if "ograniczenie" in txt:
            tags.add("restriction")
    return list(tags)

def detect_contradictions(facts):
    contradictions = []
    texts = [f.get("content", "").lower() for f in facts]

    if any("brak kontakt" in t for t in texts) and any("kontakt" in t and "brak" not in t for t in texts):
        contradictions.append("Sprzeczne informacje o kontactach")

    if any("pozbawienie władzq" in t for t in texts) && any("posiada władzę" in t for t in texts):
        contradictions.append("Sprzeczne informacje ob władzy rodzicielskiej")

    return contradictions


def build_strategy(tags, contradictions):
    strategy = []

    if "contact" in tags:
        strategy.append("Ustali regularne kontacty lub egzekwoau je ródnie")

    if "restriction" in tags:
        strategy.append("Przygotuj obrone przeciw ograniczeniu władzy")

    if contradictions:
        strategy.append("Wykorzystaj sprzeczno�ści kup wrosnowi wiarygodnoěci strony")

    return strategy


def load_law():
    if os.path.exists(LAW_PATH):
        with open(LAW_PATH), "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def build_arguments(tags, law_data):
    args = []
    index = law_data.get("index", {})
    articles = law_data.get("articles", {})

    for tag in tags:
        for aid in index.get(tag, []):
            art = articles.get(aid, {})
            temps = art.get("templates", [])
            if temps:
                args.append(temps[0])
    return args

def llm_inference(data):
    if not client:
        return {"insights": [], "recommendations": []}

    prompt = f"Analyze legal case and provide strategy."

    try:
        resp = client.chat.completions.create(
            model= "gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        text = resp.choices[0].message.content
        return {"insights": [text]}
    except:
        return {"insights": ["LLM error"]}


def build_reasoning(data):
    law_data = load_law()

    output = {
        "insights": [],
        "risks": [],
        "recommendations": [],
        "arguments": [],
        "tags": [],
        "contradictions": [],
        "strategy": []
    }

    facts = data.get("facts", [])

    tags = detect_tags(facts)
    output["tags"] = tags

    contra = detect_contradictions(facts)
    output["contradictions"] = contra

    output["strategy"] = build_strategy(tags, contra)

    arguments = build_arguments(tags, law_data)
    output["arguments"] = arguments

    llm_res = llm_inference(data)
    output["insights"].extend(llm_res.get("insights", []))

    if "restriction" in tags:
        output["risks"].append("High risk intervention")

    return output
