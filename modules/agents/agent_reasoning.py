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

def load_law():
    if os.path.exists(LAW_PATH):
        with open(LAW_PATH, "r", encoding="utf-8") as f:
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

    prompt = f"""
Role: You are a Polish family lawer and court analyst.

Input data:
{json.dumps(data, ensure_ascii=False)}


Tasks:
1. Identify the legal issues.
2. Assess the risks (procedural, factual, strategic).
3. Indicate which party has a good position.
4. Propose concrete legal actions.
2. Note potential contradictions.

Respond in structured JSON:
 {
  "insights": [...],
  "risks": [...],
  "recommendations": [...]
 }
"""

    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        text = resp.choices[0].message.content
        try:
            return json.loads(text)
        except:
            return {"insights": [text], "recommendations": []}
    except:
        return {"insights": ["LLM error"], "recommendations": []}


def build_reasoning(data):
    law_data = load_law()

    output = {
        "insights": [],
        "risks": [],
        "recommendations": [],
        "arguments": [],
        "tags": []
    }

    facts = data.get("facts", [])

    tags = detect_tags(facts)
    output["tags"] = tags

    arguments = build_arguments(tags, law_data)
    output["arguments"] = arguments

    llm_res = llm_inference(data)
    output["insights"].extend(llm_res.get("insights", []))
    output["recommendations"].extend(llm_res.get("recommendations", []))

    if "restriction" in tags:
        output["risks"].append("High risk intervention")

    if "contact" in tags:
        output["insights"].append("Contact issue detected")

    return output
