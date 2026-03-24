# CASE CORE (AGGREGATOR) — LEGAL-OS (LOSAI)

## 1. CEL

CASE CORE to centralny silnik agregujący wszystkie dane sprawy.

Łączy:
- dokumenty (ekstrakcja)
- ryzyka
- strategię
- timeline
- encje

Tworzy jeden spójny model sprawy: case.json

---

## 2. WEJŚCIE

Źródła:

- Ekstrakcja_Danych/*.json
- Outputs/risk.json
- Outputs/strategy.json

---

## 3. OUTPUT

AKTA_NSM_xxxx_xx/case.json

---

## 4. STRUKTURA CASE.JSON

{
  "case_id": "NSM_xxxx/yy",

  "documents": [],
  "entities": [],
  "child": {},

  "facts": [],
  "events": [],
  "timeline": [],

  "legal_references": [],
  "theses": [],

  "risk_analysis": {},
  "strategy": {},

  "case_state": {
    "phase": "",
    "last_update": ""
  }
}

---

## 5. LOGIKA AGREGACJI

### 5.1 DOCUMENT MERGE
- każdy dokument → dodany do listy
- deduplikacja po document_id

---

### 5.2 ENTITY RESOLUTION
- łączenie tych samych osób
- normalizacja ról

---

### 5.3 FACT MERGE
- unikalne fakty
- agregacja confidence

---

### 5.4 EVENT + TIMELINE
- sortowanie po dacie
- budowa osi czasu

---

### 5.5 RISK INJECTION
- pobranie z risk.json
- zapis do case

---

### 5.6 STRATEGY INJECTION
- pobranie z strategy.json
- zapis do case

---

## 6. CASE STATE ENGINE

Na podstawie:

- risk
- strategy
- events

ustala:

- aktualną fazę sprawy
- status

---

## 7. WNIOSEK

CASE CORE to:

→ pojedyncze źródło prawdy sprawy
→ baza dla wszystkich agentów
