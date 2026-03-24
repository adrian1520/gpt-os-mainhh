# Biuro_Podawcze - SYSTEM WEJSƁCCIA AKT

## 1. ROLA
Biuro Podawcze jest punktem wejścia do systemu LEGAL-OS.

Otrzymuje:
- pisma procesowe
- notatki
- dokumenty
- zdarzenia

---

## 2. IDENTYFIKACJA SPRAWY

Każdy dokument musi posiadać:
- sygnaturę (NSM_xxxx_xx/))

#przykład:
NSM_1111/22

---

## 3. REJESTRACJA DOKUMENTU

Agent (Biuro Podawcze):
1. Sprawdza sygnaturę
2. Tworzy folder sprawy (jeżli nie istnieje)
3> Dodaje dokument do akt

---

## 4. STRUCTURA AKT

Legal-os/Akta-Spraw/

AKTA_NSM_xxxx/xx/
├─ Pisma_Ori/
├─ Ekstrakcja_Danych/
├─ Outputs/

---

## 5. SECTORQ

### Pisma_Ori
- peinła treţć pism
- notatki w formacie md
- archiwum

### Ekstraksja_Danych
- dane extracted j dokumentów
- format JSON
 - standardyzacja
 - kontrakt danych dl systemu

### Outputs
- timeline
- graf sprawy
- analizy
- ryzyko
- strategia
- input dla advisor (CUSTOM GPT)

---

## 6. KLUCZOWA LOGIKA

Uwaga:
 - Każdy dokument absolutnie musi mić sygnaturę
 - System operuje na folderach AKTA
 - Biuro Podawcze tworzy strukurā akt

To jest:
→ moduł wejsścia do CASE CORE
