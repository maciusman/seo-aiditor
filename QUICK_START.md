# 🚀 Quick Start Guide - SEO AIditor

## Uruchom aplikację w 3 krokach (5 minut)

---

## Krok 1: Instalacja Dependencies (2 min)

### Otwórz terminal/CMD w folderze projektu:

```bash
cd x:\Aplikacje\seo-aiditor
```

### Zainstaluj wymagane biblioteki Python:

```bash
pip install -r requirements.txt
```

**Co zostanie zainstalowane:**
- Flask (API server)
- BeautifulSoup4 (HTML parsing)
- Requests (HTTP client)
- textstat (readability analysis)
- validators (URL validation)
- flask-cors (CORS support)

---

## Krok 2: Konfiguracja Google API (3 min)

### 📋 Szybka instrukcja:

1. **Idź do:** [Google Cloud Console](https://console.cloud.google.com/)
2. **Zaloguj się** (konto Gmail)
3. **Utwórz projekt:** "SEO Audit Tool"
4. **Włącz API:** Wyszukaj "PageSpeed Insights API" → ENABLE
5. **Wygeneruj klucz:** Credentials → Create Credentials → API Key
6. **Skopiuj klucz**

### 🔧 Wstaw klucz do config.py:

Otwórz `config.py` i edytuj:

```python
GOOGLE_PSI_API_KEY = "AIzaSyD...TWOJ_KLUCZ_TUTAJ"
```

**💡 Szczegółowa instrukcja:** Zobacz `GOOGLE_API_SETUP.md`

---

## Krok 3: Uruchomienie (30 sekund)

### Metoda A: Backend + Frontend (REKOMENDOWANE)

#### Terminal 1 - Uruchom Backend:
```bash
python app.py
```

**Powinieneś zobaczyć:**
```
Starting SEO AIditor API Server...
API will be available at http://localhost:5000
 * Running on http://0.0.0.0:5000
```

#### Terminal 2 - Otwórz Frontend:
```bash
# Windows:
start index.html

# Mac:
open index.html

# Linux:
xdg-open index.html
```

### Metoda B: Tylko Frontend (DEMO mode)

Jeśli nie chcesz uruchamiać backendu:

```bash
# Po prostu otwórz w przeglądarce:
start index.html
```

**Frontend automatycznie użyje mock data dla demonstracji.**

---

## ✅ Test działania

### 1. Otwórz http://localhost:5000/api/health

**Powinieneś zobaczyć:**
```json
{
  "status": "healthy",
  "service": "SEO AIditor API"
}
```

### 2. W przeglądarce wpisz URL strony do audytu:

```
https://example.com
```

### 3. Kliknij "ROZPOCZNIJ DARMOWY AUDYT"

### 4. Poczekaj ~30-60 sekund na wyniki

---

## 📊 Co dalej?

### Funkcje do wypróbowania:

✅ **Audyt SEO** - Wpisz dowolny URL
- Strona główna twojej firmy
- Blog
- Landing page
- Konkurencja (porównaj wyniki!)

✅ **Eksport wyników**
- Kliknij "Pobierz PDF" (TODO - wymaga rozbudowy)
- Kliknij "Eksportuj CSV" (działa!)
- Kliknij "Eksportuj JSON" (działa!)

✅ **Analiza kategorii**
- Kliknij na kategorie aby rozwinąć szczegóły
- Zobacz Quick Wins (priorytetowe poprawki)
- Przeczytaj rekomendacje Fix

---

## 🐛 Problemy?

### "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### "API key error"
- Sprawdź `config.py` - czy klucz jest poprawny?
- Sprawdź Google Cloud - czy API jest włączone?
- Poczekaj 2-3 minuty po utworzeniu klucza

### "CORS error"
- Upewnij się że backend (`python app.py`) działa
- Frontend musi być otwarty przez przeglądarkę (nie file://)

### "Cannot fetch page"
- Sprawdź URL - dodaj https://
- Niektóre strony blokują boty
- Zwiększ timeout w `config.py`: `REQUEST_TIMEOUT = 20`

### Szczegółowe rozwiązania:
👉 Zobacz `README.md` → Troubleshooting

---

## 📚 Dokumentacja

- **README.md** - Pełna dokumentacja
- **GOOGLE_API_SETUP.md** - Szczegóły konfiguracji API
- **CONTRIBUTING.md** - Jak współtworzyć projekt

---

## 🎯 Przykładowe strony do testowania:

```
https://example.com
https://python.org
https://github.com
https://wikipedia.org
https://your-website.com
```

---

## 💡 Pro Tips

1. **Testuj różne typy stron:**
   - E-commerce
   - Blog
   - Landing page
   - SaaS
   - Local business

2. **Porównuj wyniki:**
   - Twoja strona vs konkurencja
   - Przed i po optymalizacji
   - Desktop vs Mobile

3. **Użyj Quick Wins:**
   - Zacznij od najprostszych poprawek
   - High impact + Low effort = Szybkie efekty

4. **Monitoruj progress:**
   - Zapisuj wyniki (localStorage)
   - Eksportuj raporty
   - Śledź zmiany w czasie

---

## 🚀 Gotowe!

**Aplikacja działa!** Możesz teraz:

1. ✅ Przeprowadzać audyty SEO
2. ✅ Analizować wyniki
3. ✅ Eksportować raporty
4. ✅ Implementować poprawki

---

**Powodzenia z audytami! 🎉**

Jeśli masz pytania → Otwórz Issue na [GitHub](https://github.com/maciusman/seo-aiditor/issues)
