# Multi-Page Intelligent Site Analysis

## Przegląd

SEO AIditor może teraz analizować **całą witrynę**, a nie tylko pojedynczą stronę. System AI automatycznie wykrywa typ witryny, wybiera najbardziej reprezentatywne strony i przeprowadza **holistyczną analizę** - traktując wszystkie strony jako jedną spójną całość.

## Jak to działa?

### 🔍 Dwuetapowy proces analizy

#### **ETAP 1: Wykrywanie typu witryny i wybór stron (10-15 sekund)**

1. **Crawling strony głównej**
   - Pobieranie HTML strony głównej
   - Ekstrakcja wszystkich linków wewnętrznych
   - Próba pobrania sitemap.xml (opcjonalnie)

2. **AI wykrywa typ witryny**
   - Gemini 2.5 Flash analizuje stronę główną i dostępne linki
   - Identyfikuje typ: **e-commerce, usługi, blog, firma, portfolio**
   - Zwraca poziom pewności (0-100%)

3. **AI wybiera 4 dodatkowe strony**
   - Strony są dobierane inteligentnie na podstawie typu witryny
   - Każda strona reprezentuje inny aspekt biznesu
   - AI wyjaśnia, dlaczego każda strona została wybrana

**Przykładowe wybory:**

| Typ witryny | Wybrane strony |
|-------------|----------------|
| **E-commerce** | Strona kategorii, Strona produktu, Artykuł blogowy, O nas/Zaufanie |
| **Usługi** | Główna usługa, Dodatkowa usługa, O firmie/Zespół, Blog/Zasoby |
| **Blog** | Najnowszy artykuł, Popularny artykuł, Kategoria/Archiwum, O autorze |
| **Firma** | Produkty/Rozwiązania, O firmie, Case study, Kontakt |

#### **ETAP 2: Holistyczna analiza (30-40 sekund)**

AI analizuje **wszystkie 5 stron razem** jako **JEDNĄ WITRYNĘ**, szukając:

✅ **Wzorców w szablonach** - Problemy powtarzające się na wielu stronach
✅ **Spójności treści** - Czy brand voice jest jednolity?
✅ **Strategii konwersji** - Analiza całego lejka sprzedażowego
✅ **Sygnałów E-E-A-T** - Wiarygodność na poziomie całej witryny
✅ **Luk w strategii** - Brakujące krytyczne strony

## Wyniki analizy multi-page

### 📊 Zakładka: Przegląd (Overview)

- **Podsumowanie wykonawcze** - 2-3 zdania o stanie witryny i największych szansach
- **3 wyniki:**
  - Wynik strony głównej (0-100)
  - Wynik holistyczny (0-100) - całościowa ocena SEO
  - Liczba przeanalizowanych stron (zwykle 5)
- **Podgląd stron** - Lista wszystkich przeanalizowanych stron z powodami wyboru
- **Eksport** - CSV i JSON

### 📄 Zakładka: Strony (Pages)

- **Strona główna:**
  - Pełny audyt techniczny (wszystkie kategorie)
  - On-page SEO, indeksowanie, treść, PageSpeed
  - AI Content Quality, E-E-A-T

- **Dodatkowe strony (4):**
  - Podstawowe informacje (URL, typ, powód wyboru)
  - Oczekiwane spostrzeżenia
  - **Uwaga:** Dla dodatkowych stron nie robimy pełnego crawlingu, tylko analiza AI

**Mobile:** Dropdown do wyboru strony
**Desktop:** Sidebar z listą stron (sticky)

### 🎨 Zakładka: Szablony (Templates)

**KLUCZOWA NOWOŚĆ!**

Pokazuje problemy na poziomie szablonów, które wpływają na **wiele stron jednocześnie**.

**Każdy szablon zawiera:**
- Nazwa szablonu (np. "product_page", "category_page")
- **Liczba stron, których dotyczy** (np. "~50 stron produktowych")
- **Wpływ SEO:** HIGH | MEDIUM | LOW
- **Trudność naprawy:** EASY | MEDIUM | HARD
- **Krytyczne problemy** - Lista konkretnych błędów
- **Wpływ biznesowy** - Jak to wpływa na przychody/leady/ruch
- **Zalecana naprawa** - Konkretne kroki do wykonania
- **Oczekiwana poprawa** - Szacunkowy efekt (np. "+30% ruchu organicznego")

**Dlaczego to ważne?**
Naprawienie 1 szablonu = naprawienie dziesiątek lub setek stron! 🚀

### ⚠️ Zakładka: Problemy (Issues)

Zbiera **wszystkie problemy** ze wszystkich przeanalizowanych stron.

**Funkcje:**
- **Sortowanie:** Według wpływu lub wagi
- **Filtrowanie:** Krytyczne, Ważne, Rekomendacje
- **Źródła:** Problemy ze strony głównej + problemy międzystronowe

**Problemy międzystronowe** - wykryte przez AI:
- Problem obecny na wielu stronach
- Przyczyna źródłowa (root cause)
- Zalecane rozwiązanie systemowe

### 🎯 Zakładka: Strategia (Strategy)

#### **Strategia witryny**
- Główny cel biznesowy (zidentyfikowany przez AI)
- Jasność grupy docelowej (0-100)
- Siła propozycji wartości (0-100)
- Pozycjonowanie konkurencyjne

#### **Lejek konwersji**
- **Obecne etapy:** awareness → consideration → decision → action
- **Luki w lejku:** Brakujące lub słabe punkty
- **Spójność CTA:** (0-100)
- **Efektywność CTA:** Analiza jakości wezwań do działania
- **Punkty tarcia:** Przeszkody w konwersji
- **Szybkie wygrane konwersji:** Małe zmiany, duży wpływ

#### **Skalowalne rekomendacje**

Każda rekomendacja zawiera:
- **Priorytet:** CRITICAL | HIGH | MEDIUM | LOW
- **Kategoria:** TEMPLATE | CONTENT | TECHNICAL | UX
- **Zakres:** Ile stron/elementów dotyczy
- **Wpływ biznesowy:** Konkretny wpływ na biznes
- **Kroki wdrożenia:** 1, 2, 3... (szczegółowa instrukcja)
- **Szacowany czas:** godziny/dni
- **Odpowiedzialny:** developer | marketer | copywriter | designer
- **Metryka sukcesu:** Jak zmierzyć efekt

#### **Mapa drogowa (Roadmap)**

Podzielona na 4 sekcje:
- **Tydzień 1 (Pilne):** Natychmiastowe akcje z najwyższym ROI
- **Miesiąc 1:** Fundamentalne ulepszenia
- **Miesiąc 3:** Strategiczne inicjatywy SEO i contentowe
- **Ciągłe działania:** Praktyki do wdrożenia na stałe

## Konfiguracja

### Włączenie/wyłączenie multi-page

W pliku [`config.py`](config.py):

```python
# Multi-Page Analysis
ENABLE_MULTI_PAGE_ANALYSIS = True  # Ustaw False, aby wyłączyć
MAX_PAGES_TO_ANALYZE = 5  # Maks. stron per audyt (włącznie ze stroną główną)
MULTI_PAGE_TIMEOUT = 60  # Timeout w sekundach
```

### Wymagania

- **AI musi być włączone:** `ENABLE_AI_ANALYSIS = True`
- **Klucz API Gemini:** Poprawnie skonfigurowany w `config_local.py`
- **Połączenie internetowe:** Do pobierania dodatkowych stron

## Architektura techniczna

### Backend (Python)

**Nowe pliki:**

1. **[site_crawler.py](site_crawler.py)**
   - `crawl_homepage()` - Crawling strony głównej + ekstrakcja linków
   - `fetch_selected_pages()` - Równoległe pobieranie stron (ThreadPoolExecutor)
   - `attempt_sitemap_fetch()` - Próba pobrania sitemap.xml
   - `extract_page_metadata()` - Wyciąganie title, meta desc, H1, word count

2. **[analyzers/ai_site_structure.py](analyzers/ai_site_structure.py)**
   - `detect_site_type_and_select_pages()` - **ETAP 1:** AI wykrywa typ i wybiera strony
   - Wspiera języki: PL, EN, DE, ES, FR
   - Zwraca: typ witryny, confidence, charakterystykę, wybrane strony

3. **[analyzers/ai_multi_page.py](analyzers/ai_multi_page.py)**
   - `analyze_site_holistically()` - **ETAP 2:** Holistyczna analiza
   - Prompt skupiony na: szablonach, wzorcach, skalowalnych rozwiązaniach
   - Zwraca: holistic_score, template_insights, scalable_recommendations, roadmap

**Zaktualizowane pliki:**

- **[audit_engine.py](audit_engine.py):**
  - Nowa funkcja `run_audit(url, multi_page=None)`
  - Dwuetapowy flow: homepage audit → multi-page analysis
  - Graceful fallback do single-page przy błędach
  - Nowa struktura odpowiedzi dla multi-page

- **[ai_engine.py](ai_engine.py):**
  - Nowa metoda `analyze_multiple_urls(urls, prompt)`
  - Wsparcie dla batch URL analysis w Gemini

### Frontend (React)

**Całkowita przebudowa [index.html](index.html):**

**Komponenty:**
- `App` - Główna aplikacja
- `SinglePageResults` - Wyniki single-page (backward compatible)
- `MultiPageResults` - Wyniki multi-page z tab navigation
- `OverviewTab` - Zakładka przeglądu
- `PagesTab` - Zakładka stron (sidebar/dropdown)
- `TemplatesTab` - Zakładka szablonów
- `IssuesTab` - Zakładka problemów (sortowanie/filtrowanie)
- `StrategyTab` - Zakładka strategii

**Responsive:**
- **Mobile-first design**
- `@media (min-width: 768px)` dla desktop
- Dropdown na mobile, sidebar na desktop
- Ikony na małych ekranach, pełne labele na dużych

## Przykładowa struktura odpowiedzi

```json
{
  "audit_type": "multi-page",
  "url": "https://example.com",
  "timestamp": "2025-01-02T...",
  "language": "pl",
  "site_type": "e-commerce",
  "site_type_confidence": 95,
  "site_characteristics": {
    "primary_purpose": "Sprzedaż produktów elektronicznych",
    "target_audience": "Konsumenci B2C",
    "monetization_model": "E-commerce",
    "content_focus": "Produkty + porady techniczne"
  },
  "pages_analyzed": 5,

  "homepage": {
    "audit_type": "single-page",
    "categories": { ... },
    "final_score": 72,
    "grade": { ... }
  },

  "additional_pages": [
    {
      "url": "https://example.com/laptopy",
      "page_type": "category",
      "selection_reason": "Shows product taxonomy",
      "expected_insights": "Template structure for all categories"
    }
  ],

  "site_wide_analysis": {
    "holistic_score": 68,
    "executive_summary": "...",
    "template_insights": [ ... ],
    "content_patterns": { ... },
    "site_strategy": { ... },
    "conversion_funnel": { ... },
    "scalable_recommendations": [ ... ],
    "cross_page_issues": [ ... ],
    "roadmap": { ... }
  },

  "final_score": 72,
  "holistic_score": 68,
  "grade": { ... }
}
```

## Koszty API

**Gemini 2.5 Flash** - bardzo ekonomiczny model:

- **Input:** $0.0001 / 1000 tokenów
- **Output:** $0.00004 / 1000 tokenów

**Szacunkowy koszt per audyt multi-page (5 stron):**

| Etap | Tokeny in | Tokeny out | Koszt |
|------|-----------|------------|-------|
| ETAP 1: Wybór stron | ~5,000 | ~500 | $0.0007 |
| ETAP 2: Holistic | ~15,000 | ~3,000 | $0.0027 |
| Inne AI (content, plan) | ~10,000 | ~2,000 | $0.0018 |
| **RAZEM** | ~30,000 | ~5,500 | **~$0.05** |

**Darmowy tier Gemini:**
1500 zapytań/dzień = **~75,000 audytów multi-page miesięcznie** 🎉

## Najlepsze praktyki

### 1. Wybór URL do audytu

✅ **Podaj URL strony głównej** (np. `https://twojadomena.pl`)
❌ Nie podawaj pojedynczych artykułów czy podstron

### 2. Interpretacja wyników

- **Wynik strony głównej** - Typowy audyt SEO tej jednej strony
- **Wynik holistyczny** - Ogólna kondycja SEO całej witryny
- **Template insights** - **PRIORYTET!** Najbardziej skalowalne zmiany

### 3. Działanie na podstawie wyników

**Kolejność wdrażania:**

1. **Templates Tab** → Napraw szablony (wysokie ROI)
2. **Strategy Tab → Roadmap → Week 1** → Pilne akcje
3. **Issues Tab** → Sortuj po Impact → Top 5-10 problemów
4. **Strategy Tab → Scalable Recommendations** → CRITICAL + HIGH
5. **Roadmap Month 1 & Month 3** → Długoterminowa strategia

## Rozwiązywanie problemów

### Multi-page nie działa

**Sprawdź:**
1. `ENABLE_MULTI_PAGE_ANALYSIS = True` w `config.py`
2. `ENABLE_AI_ANALYSIS = True` w `config.py`
3. Poprawny klucz API w `config_local.py`
4. Logi w terminalu - szukaj błędów AI

### Timeout (przekroczono limit czasu)

- Zwiększ `MULTI_PAGE_TIMEOUT` w `config.py` (np. do 90)
- Lub zmniejsz `MAX_PAGES_TO_ANALYZE` (np. do 3)

### Niewłaściwe strony wybrane przez AI

AI uczy się z kontekstu. Jeśli wybór jest nietrafny:
- Upewnij się, że strona główna ma dobre linki wewnętrzne
- Sprawdź, czy sitemap.xml jest dostępny
- AI wybiera na podstawie dostępnych linków (max 100)

### Brak template insights

AI może nie wykryć wzorców szablonów jeśli:
- Strony są zbyt różne (brak wspólnych szablonów)
- Wybrano za mało stron (zwiększ `MAX_PAGES_TO_ANALYZE`)
- Problem z parsowaniem HTML

## Roadmap funkcji

**Planowane ulepszenia:**

- [ ] PDF export z pełnym raportem multi-page
- [ ] Wizualizacja lejka konwersji (diagram flow)
- [ ] Porównanie wyników w czasie (tracking zmian)
- [ ] Integracja z Google Search Console (dane ruchu)
- [ ] Analiza konkurencji (porównanie z innymi witrynami)
- [ ] White-label raporty (brandowanie dla agencji)

## FAQ

**Q: Czy mogę wyłączyć multi-page i wrócić do single-page?**
A: Tak, ustaw `ENABLE_MULTI_PAGE_ANALYSIS = False` w `config.py`.

**Q: Czy multi-page działa bez AI?**
A: Nie. Multi-page wymaga `ENABLE_AI_ANALYSIS = True`.

**Q: Ile czasu trwa audyt multi-page?**
A: Zwykle 30-60 sekund (vs 15-20s dla single-page).

**Q: Czy mogę zmienić liczbę analizowanych stron?**
A: Tak, zmień `MAX_PAGES_TO_ANALYZE` w `config.py` (min 2, max 10).

**Q: Czy dane są gdzieś wysyłane poza moją maszynę?**
A: Tak, do Gemini API (Google) do analizy AI. Dane NIE są przechowywane przez Google.

**Q: Czy mogę użyć tego komercyjnie?**
A: Tak, ale sprawdź warunki Gemini API. Free tier ma limity.

---

**Autor:** SEO AIditor Team
**Wersja:** 2.0 (Multi-Page Intelligence)
**Data:** 2025-01-02

🤖 Powered by **Gemini 2.5 Flash**
