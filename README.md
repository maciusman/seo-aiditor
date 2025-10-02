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

### Frontend:
- **React 18** - UI framework
- **Tailwind CSS** - styling
- **Chart.js** - wizualizacje
- **Vanilla JS** - brak build tools

### API:
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

### 1. Google PageSpeed Insights API Key

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

### 2. Edytuj config.py

Otwórz `config.py` i wstaw swój API key:

```python
GOOGLE_PSI_API_KEY = "TWOJ_API_KEY_TUTAJ"
```

---

## 🚀 Uruchomienie

### Metoda 1: Backend + Frontend (pełna funkcjonalność)

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
