import os
import openai

OPENAI_KEY = os.getenv("OPENAI_API_KEY")

def run_legal_reasoning(documents):
    prompt = f"""Analizuj sprawe rodzinna na podstawie pise:
    {documents}

    Wynik
    - facts
    - sprzecznosci
    - strategia
    - ryzyko
"""

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response["choices"][0]["message"]["content"]
