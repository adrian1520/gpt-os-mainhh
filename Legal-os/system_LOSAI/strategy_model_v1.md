# STRATEGY MODEL V1 — LEGAL-OS (LOSAI)

## 1. CEL

Strategy Model V1 to silnik decyzyjny systemu Legal-OS.

System:
- określa aktualną fazę sprawy
- ustala priorytety działań
- generuje rekomendacje
- definiuje działania zabronione
- przewiduje możliwe wyniki

---

## 2. WEJŚCIE

Strategy Engine korzysta z:

- Extraction V2
- Risk Model V1
- Timeline (events)
- Case Graph

---

## 3. STRUKTURA DANYCH

{
  "strategy": {
    "phase": "defense | execution | escalation",

    "main_goal": "string",

    "priorities": [
      {
        "action": "string",
        "priority": "critical | high | medium",
        "deadline": "optional",
        "reason": "string"
      }
    ],

    "recommended_actions": [],
    "forbidden_actions": [],
    "tactical_rules": [],
    "expected_outcomes": []
  }
}

---

## 4. PHASE DETECTOR

Fazy:

- PRE_REPORT
- DEFENSE
- EXECUTION
- ESCALATION

Reguły:

- brak doręczenia + decyzja → DEFENSE
- aktywna egzekucja → EXECUTION
- działania instytucji → ESCALATION

---

## 5. PRIORITY ENGINE

Priorytet zależy od:
- severity ryzyka
- wpływu na sprawę
- czasu (deadlines)

---

## 6. ACTION GENERATOR

Na podstawie danych system generuje:

- zarzuty proceduralne
- wnioski procesowe
- działania dowodowe

---

## 7. FORBIDDEN ACTIONS

System blokuje:

- eskalację emocjonalną
- odmowę współpracy bez podstawy
- działania sprzeczne z orzeczeniem

---

## 8. TACTICAL RULES

- komunikacja neutralna
- dokumentowanie zdarzeń
- oparcie o przepisy
- koncentracja na dobru dziecka

---

## 9. OUTCOME PREDICTION

System przewiduje:

- możliwe decyzje sądu
- kierunek sprawy
- skutki działań

---

## 10. WNIOSEK

Strategy Model V1 to:

→ silnik decyzji procesowych
→ warstwa operacyjna Legal-OS
