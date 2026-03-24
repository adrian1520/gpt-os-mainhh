# RISK MODEL V1 — LEGAL-OS (LOSAI)

## 1. CEL

Risk Model V1 to system identyfikacji i oceny ryzyk procesowych w sprawach prawa rodzinnego (Polska).

System:
- wykrywa ryzyka
- klasyfikuje je
- ocenia ich wpływ
- wspiera strategię procesową

---

## 2. KATEGORIE RYZYK

### 2.1 PROCEDURAL RISK

Dotyczy naruszeń procedury:

- brak doręczenia
- brak wezwania
- brak pouczenia

Przykład:
→ brak doręczenia postanowienia

---

### 2.2 INSTITUTIONAL RISK

Dotyczy działań instytucji:

- nadmierna ingerencja
- działania bez podstaw
- presja kuratora / MOPR

---

### 2.3 STRATEGIC RISK

Dotyczy jakości prowadzenia sprawy:

- niespójność stanowiska
- brak argumentów
- brak dowodów

---

### 2.4 CHILD WELFARE RISK

Dotyczy dobra dziecka:

- realne zagrożenie
- nieprawidłowe warunki

---

### 2.5 COMPLIANCE RISK

Dotyczy zachowania strony:

- niestawiennictwo
- brak współpracy
- naruszenie obowiązków

---

## 3. STRUKTURA DANYCH

{
  "risk_analysis": {
    "global_risk": "low | medium | high",

    "risks": [
      {
        "type": "procedural",
        "subtype": "service_failure",
        "severity": "low | medium | high | critical",
        "severity_score": 1-5,
        "confidence": 0-1,
        "evidence": [],
        "impact": "string"
      }
    ]
  }
}

---

## 4. LOGIKA SILNIKA

### RULE 1: brak doręczenia

IF:
- brak doręczenia
- brak wezwania

THEN:
→ procedural_risk = CRITICAL

---

### RULE 2: brak zagrożeń dziecka

IF:
- wielokrotne wizyty
- brak zagrożeń

THEN:
→ child_welfare_risk = LOW

---

### RULE 3: presja instytucji bez podstaw

THEN:
→ institutional_risk = HIGH

---

### RULE 4: spójna argumentacja

THEN:
→ strategic_risk = LOW

---

## 5. SYSTEM SCORINGU

Każde ryzyko:

- severity_score (1-5)
- confidence (0-1)

Global risk:
→ agregacja ważona

---

## 6. OUTPUT

System generuje:

- listę ryzyk
- ich ocenę
- wpływ na sprawę
- rekomendacje strategiczne

---

## 7. WNIOSEK

Risk Model V1 to:

→ fundament podejmowania decyzji procesowych
→ kluczowa warstwa Legal Intelligence
