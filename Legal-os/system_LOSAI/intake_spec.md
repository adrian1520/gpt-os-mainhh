# INTAKE SYSTEM SPEC — LEGAL-OS (LOSAI)

## 1. CEL

INTAKE (Biuro Podawcze) to krytyczny moduł wejścia do systemu Legal-OS.

Każdy dokument, notatka lub zdarzenie MUSI przejść przez intake.

Zasada:
→ jakość wejścia = jakość całego systemu

---

## 2. TYPY WEJŚCIA

entry_type:

- document (pisma procesowe)
- note (notatki wewnętrzne)
- evidence (dowody)
- event (zdarzenia)

---

## 3. CONTRACT WEJŚCIA

Każdy wpis MUSI zawierać:

{
  "entry_id": "string",
  "entry_type": "document | note | evidence | event",
  "case_signature": "NSM_xxxx/yy",
  "title": "string",
  "content": "string",
  "created_at": "timestamp",
  "source": "user | system | external"
}

---

## 4. WALIDACJA

System odrzuca wpis jeśli:

- brak case_signature
- błędny format sygnatury
- pusty content

---

## 5. NORMALIZACJA SYGNATURY

NSM_1111/22 → AKTA_NSM_1111_22

---

## 6. PIPELINE

1. Walidacja
2. Normalizacja
3. Resolve case (create if not exists)
4. Generowanie ID dokumentu
5. Zapis do Pisma_Ori
6. Trigger ekstrakcji

---

## 7. STRUKTURA AKT

AKTA_NSM_1111_22/

├── Pisma_Ori/
├── Ekstrakcja_Danych/
└── Outputs/

---

## 8. FORMAT PISMA (Pisma_Ori)

# META

entry_id: ...
entry_type: ...
case_signature: ...
created_at: ...

---

# TYTUŁ

...

---

# TREŚĆ

...

---

## 9. EKSTRAKCJA

Po zapisie tworzony jest plik:

Ekstrakcja_Danych/doc_xxx.json

Zgodny z:
extraction_schema.json

---

## 10. BEZPIECZEŃSTWO

- deduplikacja (hash)
- logowanie operacji
- kontrola błędów

---

## 11. ROLA CUSTOM GPT

Custom GPT:
- przyjmuje dane
- buduje intake
- zapisuje do repo
- uruchamia pipeline

---

## 12. WNIOSEK

INTAKE to:

→ oficjalna rejestracja zdarzenia w sprawie

→ fundament całego Legal-OS
