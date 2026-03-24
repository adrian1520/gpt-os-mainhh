# PARSER SPEC — LEGAL-OS (LOSAI)

## 1. CEL

Parser to silnik przekształcający dokumenty z:
→ Pisma_Ori (tekst)

do:
→ Ekstrakcja_Danych (JSON zgodny ze schemą)

Parser jest wyspecjalizowany dla:
→ prawa rodzinnego (Polska)

---

## 2. ARCHITEKTURA PARSERA

Parser składa się z modułów:

1. signature_parser
2. document_classifier
3. parties_extractor
4. child_extractor
5. requests_extractor
6. facts_extractor
7. events_extractor
8. legal_extractor

---

## 3. MODULE SPEC

### 3.1 SIGNATURE PARSER

Cel:
- wykrycie sygnatury sprawy

Regex:
[IVX]+ Nsm \d+/\d+

Output:
{
  "signature": "III Nsm 756/25"
}

---

### 3.2 DOCUMENT CLASSIFIER

Cel:
- klasyfikacja dokumentu

Typy:

- wniosek
- oświadczenie
- stanowisko
- postanowienie
- wezwanie

Reguły:

- zawiera "Wnoszę o" → wniosek
- zawiera "postanawia" → postanowienie
- zawiera "wzywa" → wezwanie
- zawiera "oświadczam" → oświadczenie

Output:
{
  "document_type": "wniosek"
}

---

### 3.3 PARTIES EXTRACTOR

Cel:
- wykrycie stron i ról

Wzorce:
- Wnioskodawca
- Uczestnik
- ojciec
- matka
- babcia

Output:
{
  "parties": [
    {
      "role": "ojciec",
      "name": "Adrian Adamowicz"
    }
  ]
}

---

### 3.4 CHILD EXTRACTOR

Cel:
- wykrycie małoletniego

Wzorce:
- "małoletni"
- "dziecko"

Output:
{
  "child": {
    "name": "Dawid Adamowicz",
    "birth_date": "2020-01-19"
  }
}

---

### 3.5 REQUESTS EXTRACTOR

Cel:
- lista żądań

Wzorce:
- "Wnoszę o"
- listy numerowane

Output:
{
  "requests": [
    "uchylenie postanowienia",
    "zabezpieczenie"
  ]
}

---

### 3.6 FACTS EXTRACTOR

Cel:
- wyodrębnienie faktów

Źródło:
- uzasadnienie
- sekcje opisowe

Output:
{
  "facts": [
    {
      "content": "...",
      "confidence": 0.8
    }
  ]
}

---

### 3.7 EVENTS EXTRACTOR

Cel:
- wykrycie zdarzeń

Wzorce:
- daty (DD.MM.YYYY)

Output:
{
  "events": [
    {
      "date": "2025-10-03",
      "description": "kontakt z kuratorem"
    }
  ]
}

---

### 3.8 LEGAL EXTRACTOR

Cel:
- wykrycie przepisów

Wzorce:
art. xxx k.p.c.
art. xxx k.r.o.

Output:
{
  "legal_references": [
    {
      "code": "k.p.c.",
      "article": "577"
    }
  ]
}

---

## 4. OUTPUT FINALNY

Parser generuje JSON zgodny z:

extraction_schema.json

---

## 5. KLUCZOWE ZAŁOŻENIA

- parser NIE jest uniwersalny
- parser jest dopasowany do polskiego prawa rodzinnego
- parser operuje na realnych wzorcach dokumentów

---

## 6. PIPELINE

Pisma_Ori → Parser → Ekstrakcja_Danych → CASE CORE

---

## 7. WNIOSEK

Parser to:

→ pierwszy silnik inteligencji systemu
→ fundament dalszych analiz (risk, strategy, AI)
