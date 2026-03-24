# EXTRACTION V2 SPEC — LEGAL-OS (LOSAI)

## 1. CEL

Extraction V2 to rozszerzony silnik analizy dokumentów prawnych.

System nie tylko ekstraktuje dane, ale:
- interpretuje znaczenie
- ocenia merytorycznie
- identyfikuje ryzyka
- buduje strategię

---

## 2. ROZSZERZONY MODEL DANYCH

{
  "document_type": "...",

  "entities": [],
  "child": {},

  "facts": [],
  "events": [],

  "requests": [],
  "legal_references": [],

  "theses": [],
  "positions": [],

  "institutional_actions": [],
  "pressure_signals": [],

  "language_assessment": {},
  "legal_assessment": {},

  "risk_analysis": {},
  "strategy": {}
}

---

## 3. MODUŁY ANALITYCZNE

### 3.1 THESIS EXTRACTOR
- wykrywa tezy procesowe
- np. brak więzi, brak podstaw, ingerencja

---

### 3.2 INSTITUTIONAL ANALYZER
- identyfikuje działania instytucji
- sąd, MOPR, kurator

---

### 3.3 PRESSURE DETECTOR
- wykrywa przymus i presję
- klasyfikacja poziomu (low → coercive)

---

### 3.4 LEGAL CONSISTENCY ENGINE
- porównuje stan faktyczny z przepisami
- wykrywa niespójności

---

### 3.5 LANGUAGE ANALYZER
- ocena stylu pisma
- formalność
- emocjonalność
- zgodność z językiem sądowym

---

### 3.6 RISK ENGINE

Analizuje:
- ryzyko decyzji sądu
- ryzyko eskalacji
- ryzyko instytucjonalne

---

### 3.7 STRATEGY ENGINE

Buduje:
- cel główny
- argumenty
- rekomendacje działań

---

## 4. ANALIZA MERYTORYCZNA

System ocenia:

- poprawność logiczną
- zgodność z prawem
- jakość argumentacji
- potencjalne błędy procesowe

---

## 5. OUTPUT

Extraction V2 generuje:

→ dane strukturalne
→ ocenę jakości pisma
→ analizę prawną
→ analizę ryzyka
→ rekomendowaną strategię

---

## 6. WNIOSEK

Extraction V2 przekształca system w:

→ Legal Intelligence System
