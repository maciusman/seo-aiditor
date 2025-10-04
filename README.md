# SEO AIditor 🚀

**Profesjonalne Narzędzie do Audytu SEO**

Kompleksowa aplikacja React + Python do przeprowadzania szczegółowych audytów SEO z profesjonalną prezentacją wyników.

---

## 📋 Spis treści

- [Funkcje](#funkcje)
- [Stack Technologiczny](#stack-technologiczny)
- [Instalacja](#instalacja)
- [Konfiguracja](#konfiguracja)
- [Uruchomienie](#uruchomienie)
- [Struktura Projektu](#struktura-projektu)
- [API Endpoints](#api-endpoints)
- [Kategorie Audytu](#kategorie-audytu)
- [Eksport Raportów](#eksport-raportów)
- [Troubleshooting](#troubleshooting)

---

## ✨ Funkcje

### 🌐 **NEW: Multi-Page Intelligent Site Analysis**

**Cała witryna, nie tylko jedna strona!**

SEO AIditor analizuje teraz do **5 stron jednocześnie** w podejściu **holistycznym**:

1. **AI wykrywa typ witryny** (e-commerce/usługi/blog/firma)
2. **AI wybiera 4 reprezentatywne strony** (np. kategoria, produkt, blog, o nas)
3. **AI analizuje wszystko razem** jako jedną spójną strategię

**Co zyskujesz:**
- 🎨 **Template-level insights** - Napraw 1 szablon = napraw dziesiątki stron!
- 📊 **Holistic scoring** - Całościowa ocena SEO witryny
- 🎯 **Scalable recommendations** - Zmiany wpływające na wiele stron
- 🚀 **Conversion funnel analysis** - Analiza całego lejka sprzedażowego
- 📅 **Strategic roadmap** - Plan działania na Week 1 / Month 1 / Month 3

**Nowy UI z zakładkami:**
- **Overview** - Podsumowanie + wyniki
- **Pages** - Szczegóły każdej strony (sidebar/dropdown)
- **Templates** - Skalowalne naprawy szablonów ⭐
- **Issues** - Wszystkie problemy (sortowanie/filtrowanie)
- **Strategy** - Roadmap + lejek konwersji

💰 **Cost:** ~$0.05 per multi-page audit (still practically FREE!)
📱 **Mobile-first UI** - Świetnie działa na telefonach i tabletach

[→ See Multi-Page Documentation](MULTI_PAGE_ANALYSIS.md)

---

### 🤖 **AI-Powered Analysis (Gemini 2.5 Flash)**
- **AI Content Quality Analysis**
  - Auto language detection (PL/EN/DE/ES/FR)
  - E-E-A-T signals detection (Experience, Expertise, Authoritativeness, Trust)
  - Search intent matching (informational/transactional/navigational/commercial)
  - Content depth and gap analysis
  - Business value assessment (audience clarity, value prop, differentiation)
  - Conversion optimization analysis
  - Competitor advantage insights

- **AI Personalized Action Plan**
  - 30/60/90-day implementation roadmap
  - Quick wins identification (high impact, low effort)
  - Prioritized tasks with impact estimates
  - Role assignments (developer/marketer/copywriter)
  - Risk assessment
  - Success metrics
  - Brutally honest recommendations

💰 **Cost (single-page):** ~$0.01-0.03 per audit (practically FREE!)
📊 **Free Tier:** 1,500 requests/day = ~75,000 multi-page audits/month!

[→ See AI Setup Guide](GEMINI_API_SETUP.md)

---

### Analiza SEO (50+ parametrów):

**🔧 Fundamenty Techniczne (20% wagi)**
- Status HTTP i dostępność
- SSL/HTTPS check
- Time to First Byte (TTFB)
- Security headers (HSTS, CSP, X-Frame-Options, etc.)
- Core Web Vitals via Google PageSpeed Insights API

**📝 Elementy On-Page (25% wagi)**
- Title tag (długość, struktura, optymalizacja)
- Meta description
- Hierarchia nagłówków H1-H6
- Alt teksty w obrazach
- Open Graph tags (social media)
- Linki wewnętrzne/zewnętrzne

**🔍 Indeksowanie & Crawlability (20% wagi)**
- Robots.txt (analiza, walidacja)
- Sitemap.xml (struktura, ilość URL)
- Canonical tags
- Meta robots
- Schema Markup (JSON-LD)

**📄 Jakość Treści & UX (20% wagi)**
- Word count i thin content detection
- Text-to-HTML ratio
- Readability score (Flesch Reading Ease)
- Keyword density
- Analiza paragrafów

**⚡ Wydajność (15% wagi)**
- LCP (Largest Contentful Paint)
- FID (First Input Delay)
- CLS (Cumulative Layout Shift)
- Mobile performance

### Dodatkowe funkcje:
- 📊 **Scoring Algorithm** - wynik końcowy 0-100
- 🎯 **Quick Wins** - priorytetowe rekomendacje
- 📈 **Business Impact Calculator** - szacowanie wzrostu ruchu
- 📄 **Export** - PDF, CSV, JSON
- 💾 **localStorage** - cache wyników
- 🎨 **Responsywny design** - mobile-first

---

## 🛠 Stack Technologiczny

### Backend:
- **Python 3.8+**
- **Flask** - REST API
- **BeautifulSoup4** - HTML parsing
- **Requests** - HTTP client
- **textstat** - readability analysis
- **validators** - URL validation
- **google-genai** - Gemini AI integration

### Frontend:
- **React 18** - UI framework
- **Tailwind CSS** - styling
- **Chart.js** - wizualizacje
- **Vanilla JS** - brak build tools

### AI & APIs:
- **Google Gemini 2.5 Flash** - AI content analysis & action plans
- **Google PageSpeed Insights API** - Core Web Vitals

---

## 📦 Instalacja

### Wymagania wstępne:
- Python 3.8 lub nowszy
- pip (package manager)
- Przeglądarka internetowa (Chrome, Firefox, Safari)

### Krok 1: Sklonuj repozytorium
```bash
git clone https://github.com/twoj-username/seo-aiditor.git
cd seo-aiditor
```

### Krok 2: Zainstaluj zależności Python
```bash
pip install -r requirements.txt
```

---

## ⚙️ Konfiguracja

### 1. Google Gemini API Key (AI Features) 🤖

**NOWE! Aby włączyć funkcje AI (5 minut):**

1. Przejdź do [Google AI Studio](https://aistudio.google.com/apikey)
2. Zaloguj się (konto Gmail)
3. Kliknij "Create API Key"
4. Wybierz "Create API key in new project"
5. Skopiuj klucz (zaczyna się od `AIza...`)

**W pliku `config_local.py` wstaw klucz:**
```python
GEMINI_API_KEY = "AIzaSy_TWOJ_KLUCZ_TUTAJ"
```
(Toggle AI: ustaw `ENABLE_AI_ANALYSIS = False` w `config.py` aby wyłączyć)

**Limity darmowe:**
- ✅ 1,500 zapytań/dzień
- ✅ 1 milion tokenów/minutę
- ✅ ~50 audytów dziennie CAŁKOWICIE ZA DARMO
- 💰 Koszt audytu: $0.01-0.03 (prawie darmowe!)

📚 **Pełna instrukcja:** [GEMINI_API_SETUP.md](GEMINI_API_SETUP.md)

---

### 2. Google PageSpeed Insights API Key

**Aby uzyskać darmowy API key (5 minut):**

1. Przejdź do [Google Cloud Console](https://console.cloud.google.com/)
2. Zaloguj się (konto Gmail)
3. Utwórz nowy projekt:
   - Kliknij dropdown przy logo Google Cloud
   - "New Project" → Nazwa: "SEO Audit Tool" → "Create"
4. Włącz PageSpeed Insights API:
   - Menu: "APIs & Services" → "Library"
   - Wyszukaj: "PageSpeed Insights API"
   - Kliknij kartę API → "ENABLE"
5. Wygeneruj API Key:
   - "APIs & Services" → "Credentials"
   - "+ CREATE CREDENTIALS" → "API key"
   - Skopiuj klucz

**Limity darmowe:**
- ✅ 25,000 zapytań/dzień
- ✅ Bez kosztów
- ✅ Wystarczy na ~800 audytów dziennie

### 3. Edytuj config_local.py

Otwórz `config_local.py` i wstaw oba klucze:

```python
# PageSpeed API
GOOGLE_PSI_API_KEY = "TWOJ_PSI_KEY_TUTAJ"

# Gemini AI (opcjonalny - ale bardzo zalecany!)
GEMINI_API_KEY = "TWOJ_GEMINI_KEY_TUTAJ"
```

⚠️ **Uwaga:** Plik `config_local.py` jest gitignored - Twoje klucze są bezpieczne!

---

## 🚀 Uruchomienie

### ⚡ Metoda 1: Automatyczne uruchomienie (ZALECANE!)

**Windows:**
```bash
# Kliknij dwukrotnie na:
start.bat
```

**Mac/Linux:**
```bash
python start.py
```

Aplikacja uruchomi się automatycznie i otworzy w przeglądarce! 🎉

---

### 🔧 Metoda 2: Ręczne uruchomienie

**Terminal 1 - Backend API:**
```bash
python app.py
```
API będzie dostępne pod: `http://localhost:5000`

**Terminal 2 - Frontend:**
```bash
# Otwórz index.html w przeglądarce
# Windows:
start index.html

# Mac:
open index.html

# Linux:
xdg-open index.html
```

### Metoda 2: Tylko Frontend (demo mode)

Jeśli backend nie jest uruchomiony, frontend automatycznie przełączy się na **mock data** dla demonstracji.

```bash
# Po prostu otwórz index.html w przeglądarce
```

### Metoda 3: Test backendu (CLI)

```bash
python audit_engine.py
```

To uruchomi przykładowy audyt dla `https://example.com` i wyświetli wyniki w konsoli.

---

## 📁 Struktura Projektu

```
seo-aiditor/
├── analyzers/                 # Moduły analizy
│   ├── __init__.py
│   ├── technical.py          # Analiza techniczna
│   ├── onpage.py             # Elementy on-page
│   ├── indexing.py           # Robots, sitemap, canonical
│   ├── content.py            # Jakość treści
│   └── pagespeed.py          # Core Web Vitals (Google API)
│
├── app.py                    # Flask API Server
├── audit_engine.py           # Główna logika audytu
├── config.py                 # Konfiguracja (API keys, thresholds)
├── utils.py                  # Funkcje pomocnicze
│
├── index.html                # Frontend React (standalone)
│
├── requirements.txt          # Zależności Python
└── README.md                 # Ta dokumentacja
```

---

## 🌐 API Endpoints

### `GET /`
Strona główna API z informacjami

### `GET /api/health`
Health check - status serwera

**Response:**
```json
{
  "status": "healthy",
  "service": "SEO AIditor API"
}
```

### `POST /api/audit`
Uruchom audyt SEO

**Request Body:**
```json
{
  "url": "https://example.com"
}
```

**Response:**
```json
{
  "url": "https://example.com",
  "timestamp": "2024-01-15T10:30:00",
  "final_score": 78.5,
  "grade": {
    "label": "GOOD",
    "emoji": "🟡",
    "color": "lightgreen"
  },
  "categories": {
    "technical": { "score": 85, "checks": {...}, "issues": [...] },
    "onpage": { "score": 72, "checks": {...}, "issues": [...] },
    "indexing": { "score": 80, "checks": {...}, "issues": [...] },
    "content": { "score": 65, "checks": {...}, "issues": [...] }
  },
  "all_issues": [...],
  "quick_wins": [...]
}
```

### `POST /api/export/json`
Eksportuj wyniki jako JSON

### `POST /api/export/csv`
Eksportuj wyniki jako CSV

---

## 📊 Kategorie Audytu

### 1. Fundamenty Techniczne (20%)
| Check | Opis | Scoring |
|-------|------|---------|
| HTTP Status | 200 OK | 100 pkt = 200, 0 pkt = inne |
| SSL/HTTPS | Certyfikat SSL | 100 pkt = HTTPS, 0 pkt = HTTP |
| TTFB | Time to First Byte | <600ms = 100, 600-1200ms = 50, >1200ms = 0 |
| Security Headers | HSTS, CSP, X-Frame, etc. | % obecnych nagłówków |

### 2. On-Page (25%)
| Check | Opis | Optimal |
|-------|------|---------|
| Title | Długość title tag | 50-60 znaków |
| Meta Desc | Meta description | 150-160 znaków |
| H1 | Liczba H1 | 1 (tylko jeden) |
| Alt Images | Obrazy z alt | 90-100% |
| Open Graph | OG tags | 3-4 tags |

### 3. Indeksowanie (20%)
| Check | Opis | Pass/Fail |
|-------|------|-----------|
| Robots.txt | Istnienie i poprawność | Istnieje, nie blokuje |
| Sitemap | XML sitemap | Istnieje, <50k URLs |
| Canonical | Canonical tags | Poprawny self-referencing |
| Meta Robots | Index/Noindex | Brak noindex |
| Schema | Structured data | JSON-LD present |

### 4. Content & UX (20%)
| Check | Opis | Optimal |
|-------|------|---------|
| Word Count | Ilość słów | 600-1500+ |
| Text/HTML Ratio | Stosunek tekstu do kodu | >15% |
| Readability | Flesch Reading Ease | >50 (łatwy do czytania) |
| Keyword Density | Gęstość słów kluczowych | 1-3% |

---

## 📥 Eksport Raportów

### PDF Export (TODO - rozbudowa)
```javascript
// Frontend feature - wymaga biblioteki jsPDF
button.onClick = () => exportToPDF(results);
```

### CSV Export
```bash
curl -X POST http://localhost:5000/api/export/csv \
  -H "Content-Type: application/json" \
  -d '{"results": {...}}'
```

### JSON Export
```bash
curl -X POST http://localhost:5000/api/export/json \
  -H "Content-Type: application/json" \
  -d '{"results": {...}}'
```

---

## 🐛 Troubleshooting

### Problem: "ModuleNotFoundError: No module named 'flask'"
**Rozwiązanie:**
```bash
pip install -r requirements.txt
```

### Problem: "API key error" w PageSpeed
**Rozwiązanie:**
1. Sprawdź czy API key jest poprawnie wpisany w `config.py`
2. Upewnij się że PageSpeed Insights API jest włączone w Google Cloud
3. Sprawdź limity (25k/dzień)

### Problem: CORS error w przeglądarce
**Rozwiązanie:**
- Upewnij się że backend (`app.py`) jest uruchomiony
- CORS jest już skonfigurowany w Flask (`flask-cors`)
- Sprawdź czy frontend wywołuje `http://localhost:5000` (nie https)

### Problem: "Cannot fetch page"
**Możliwe przyczyny:**
- URL jest niepoprawny (dodaj https://)
- Strona blokuje boty (niektóre strony mają protection)
- Timeout - strona ładuje się >10 sekund

**Rozwiązanie:**
- Sprawdź URL w przeglądarce
- Zwiększ timeout w `config.py`: `REQUEST_TIMEOUT = 20`

### Problem: Wyniki są niepełne
**Rozwiązanie:**
- Sprawdź logi w konsoli (`python app.py`)
- Niektóre strony mogą nie mieć wszystkich elementów (np. brak schema)
- To normalne - narzędzie raportuje braki jako issues

---

## 📈 Roadmap (Przyszłe Funkcje)

- [ ] PDF export z brandingiem
- [ ] Historical tracking (porównanie audytów)
- [ ] Competitive analysis (porównaj z konkurencją)
- [ ] AI-powered recommendations (Claude API)
- [ ] Local SEO module (NAP, GMB)
- [ ] Backlink profile preview
- [ ] Email report sender
- [ ] Multi-language support

---

## 🤝 Contributing

Pull requests są mile widziane! Dla większych zmian, otwórz issue aby przedyskutować co chciałbyś zmienić.

---

## 📄 Licencja

[MIT](https://choosealicense.com/licenses/mit/)

---

## 👨‍💻 Autor

Stworzone z ❤️ dla specjalistów SEO

---

## 🙏 Podziękowania

- Google PageSpeed Insights API
- BeautifulSoup4 team
- React & Tailwind CSS communities
- Claude AI (Anthropic)

---

**🚀 Powodzenia z audytami SEO!**
#   A u t o - d e p l o y m e n t   t e s t  
  
 < ! - -   A u t o - d e p l o y m e n t   t e s t   1 0 / 0 4 / 2 0 2 5   1 2 : 3 8 : 4 2   - - >  
  
 < ! - -   F i n a l   w e b h o o k   t e s t   1 0 / 0 4 / 2 0 2 5   1 2 : 5 2 : 4 8   - - >  
  
 < ! - -   U l t i m a t e   w e b h o o k   t e s t   1 0 / 0 4 / 2 0 2 5   1 3 : 0 1 : 1 3   - - >  
  
 < ! - -   '  F I N A L   A U T O - D E P L O Y M E N T   T E S T   -   1 0 / 0 4 / 2 0 2 5   1 3 : 0 7 : 4 2   - - >  
  
 < ! - -   F I N A L   W E B H O O K   T E S T   - - >  
  
 < ! - -   F I N A L   W E B H O O K   T E S T   - - >  
 