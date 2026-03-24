# LEGAL-OS (LOSAI) — SYSTEM DEFINITION

## 1. CEL SYSTEMU

Legal-OS (LOSAI) to system operacyjny dla spraw prawnych.

Jego celem jest:
- zarządzanie sprawą jako całością
- budowa cyfrowych akt sprawy
- wspieranie analizy, strategii i dokumentów

System ma działać jak:
→ „operacyjny mózg sprawy prawnej”

---

## 2. DOMENA SYSTEMU

System operuje na domenie:

### CASE (SPRAWA)

Sprawa to nadrzędna jednostka:

CASE =
- strony (uczestnicy)
- dokumenty
- fakty
- zdarzenia (timeline)
- podstawa prawna
- strategia
- ryzyko

---

## 3. STRUKTURA AKT (TARGET)

Legal-os/Akta-Spraw/{CASE_ID}/

├── case.json
├── parties.json
├── documents/
├── timeline.json
├── facts.json
├── legal_basis.json
├── risk.json
├── strategy.json
├── notes/
└── outputs/

---

## 4. KLUCZOWE OBIEKTY

### 1. CASE
Centralny obiekt systemu

### 2. DOCUMENT
Każdy dokument procesowy lub dowód

### 3. EVENT
Zdarzenie w sprawie (np. rozprawa)

### 4. FACT
Twierdzenie lub informacja

### 5. LEGAL BASIS
Powiązanie z przepisami

---

## 5. ROLA SYSTEMU

System NIE jest tylko parserem.

System jest:

- zarządcą sprawy
- budowniczym wiedzy
- generatorem dokumentów
- asystentem strategicznym

---

## 6. ROLA AGENTÓW

Agenci NIE operują na eventach.

Agenci operują na:

→ CASE CORE

Każdy agent:
- czyta case.json
- aktualizuje konkretną warstwę
- zapisuje wynik do akt sprawy

---

## 7. ARCHITEKTURA DOCELOWA

INPUT → PARSER → DOCUMENT → CASE CORE → AGENTS → OUTPUT

---

## 8. KLUCZOWY WNIOSEK

Event sourcing pozostaje warstwą techniczną.

Prawdziwy system działa na:

→ MODELU SPRAWY (CASE CORE)
