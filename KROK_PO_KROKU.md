# 🎯 KROK PO KROKU - Uruchomienie SEO AIditor

## ✅ Naprawiono błędy Windows! Teraz wszystko działa!

---

## 📋 CO MUSISZ ZROBIĆ (10 minut)

### ✅ KROK 1: Zainstaluj biblioteki (2 minuty)

**Otwórz PowerShell lub CMD w folderze projektu:**

```bash
cd x:\Aplikacje\seo-aiditor
```

**Zainstaluj biblioteki:**

```bash
pip install -r requirements.txt
```

**Powinno pokazać:**
```
Successfully installed Flask-3.0.0 flask-cors-4.0.0 requests-2.31.0 beautifulsoup4-4.12.2 textstat-0.7.3 validators-0.22.0
```

✅ **BEZ BŁĘDÓW!** (problem z lxml został naprawiony)

---

### ⚙️ KROK 2: Skonfiguruj Google API (5 minut)

**DLACZEGO:** Google PageSpeed API jest potrzebne do analizy szybkości strony (Core Web Vitals).

**JAK:**

#### 2.1 Utwórz projekt w Google Cloud

1. Idź na: **https://console.cloud.google.com/**
2. Zaloguj się (konto Gmail)
3. Kliknij **dropdown** obok "Google Cloud" → **"New Project"**
4. Nazwa: `SEO Audit Tool`
5. Kliknij **"CREATE"**

#### 2.2 Włącz PageSpeed Insights API

1. W menu (☰) wybierz: **"APIs & Services"** → **"Library"**
2. Wyszukaj: `PageSpeed Insights API`
3. Kliknij na wynik → **"ENABLE"**

#### 2.3 Wygeneruj API Key

1. **"APIs & Services"** → **"Credentials"**
2. Kliknij **"+ CREATE CREDENTIALS"**
3. Wybierz **"API key"**
4. **SKOPIUJ KLUCZ** (np. `AIzaSyD-xxxxxx`)

#### 2.4 Wstaw klucz do config.py

**Otwórz plik:** `x:\Aplikacje\seo-aiditor\config.py`

**Znajdź linię:**
```python
GOOGLE_PSI_API_KEY = "YOUR_API_KEY_HERE"
```

**Zmień na:**
```python
GOOGLE_PSI_API_KEY = "AIzaSyD-xxxxxx"  # Twój klucz tutaj
```

**ZAPISZ PLIK** (Ctrl+S)

📚 **Szczegóły:** Zobacz plik `GOOGLE_API_SETUP.md`

---

### 🚀 KROK 3: Uruchom aplikację (30 sekund)

#### OPCJA A: Automatycznie (ŁATWA)

**Kliknij dwukrotnie na plik:**
```
start.bat
```

To automatycznie uruchomi backend!

**Potem w NOWYM oknie CMD/PowerShell:**
```bash
start index.html
```

#### OPCJA B: Manualnie (2 terminale)

**Terminal 1 - Backend:**
```bash
cd x:\Aplikacje\seo-aiditor
python app.py
```

**Poczekaj aż zobaczysz:**
```
Starting SEO AIditor API Server...
 * Running on http://127.0.0.1:5000
```

**Terminal 2 - Frontend:**
```bash
cd x:\Aplikacje\seo-aiditor
start index.html
```

---

## ✅ KROK 4: Test - Czy działa?

### Test 1: Backend API

**Otwórz w przeglądarce:**
```
http://localhost:5000/api/health
```

**Powinno pokazać:**
```json
{
  "status": "healthy",
  "service": "SEO AIditor API"
}
```

✅ **Jeśli widzisz JSON → Backend działa!**

### Test 2: Frontend + Audyt

1. **W aplikacji wpisz URL:**
   ```
   https://example.com
   ```

2. **Kliknij:** `ROZPOCZNIJ DARMOWY AUDYT`

3. **Poczekaj ~30-60 sekund**

4. **Powinny pojawić się wyniki:**
   - Wynik ogólny (np. 78/100)
   - 5 kategorii audytu
   - Lista problemów
   - Quick Wins

✅ **Jeśli widzisz wyniki → Wszystko działa!** 🎉

---

## 🐛 Co jeśli coś nie działa?

### Problem 1: "ModuleNotFoundError: No module named 'flask'"

**Rozwiązanie:**
```bash
pip install -r requirements.txt
```

### Problem 2: "API key error" w wynikach

**Przyczyna:** Brak lub błędny Google API key

**Rozwiązanie:**
1. Sprawdź `config.py` - czy klucz jest wpisany?
2. Sprawdź Google Cloud - czy PageSpeed API jest włączone?
3. Poczekaj 2-3 minuty po utworzeniu klucza

### Problem 3: Backend pokazuje błąd przy starcie

**Sprawdź:**
1. Czy Python 3.8+ jest zainstalowany: `python --version`
2. Czy wszystkie biblioteki zainstalowane: `pip list`
3. Czy port 5000 nie jest zajęty (zamknij inne programy)

### Problem 4: "Cannot fetch page" podczas audytu

**Możliwe przyczyny:**
- URL niepoprawny (dodaj `https://`)
- Strona blokuje boty
- Timeout (strona wolno się ładuje)

**Rozwiązanie:**
1. Sprawdź URL w zwykłej przeglądarce
2. Spróbuj inną stronę: `https://python.org`
3. Edytuj `config.py`: zmień `REQUEST_TIMEOUT = 20`

---

## 📊 Przykładowe strony do testowania

```
https://example.com     ← Prosta strona (test)
https://python.org      ← Open source site
https://github.com      ← Tech platform
https://wikipedia.org   ← Content-heavy site
```

**Potem przetestuj swoją stronę!**

---

## 🎯 Co dalej?

### 1. Audytuj swoją stronę:
```
https://twoja-strona.pl
```

### 2. Zobacz wyniki:
- Wynik ogólny (0-100)
- Problemy do naprawy
- Quick Wins (priorytetowe poprawki)

### 3. Eksportuj raport:
- Kliknij **"Eksportuj CSV"** → otwórz w Excel
- Kliknij **"Eksportuj JSON"** → integracje

### 4. Implementuj poprawki:
- Zacznij od **Quick Wins** (high impact + low effort)
- Zobacz rozwiązania (Fix) przy każdym problemie
- Testuj ponownie po zmianach

### 5. Porównaj z konkurencją:
```
https://konkurent1.pl
https://konkurent2.pl
```

---

## 📚 Dodatkowa pomoc

**Dokumentacja:**
- `START_HERE.md` - Główny punkt wejścia
- `QUICK_START.md` - Szybki start
- `WINDOWS_FIX.md` - Info o naprawie błędów Windows
- `README.md` - Pełna dokumentacja
- `GOOGLE_API_SETUP.md` - Szczegóły Google API

**GitHub:**
- Issues: https://github.com/maciusman/seo-aiditor/issues
- Repository: https://github.com/maciusman/seo-aiditor

---

## ✅ Checklist końcowy

Sprawdź czy wszystko zrobiłeś:

- [ ] ✅ Zainstalowano biblioteki: `pip install -r requirements.txt`
- [ ] ✅ Google API key wygenerowany
- [ ] ✅ API key wpisany w `config.py`
- [ ] ✅ Backend uruchomiony: `python app.py`
- [ ] ✅ http://localhost:5000/api/health → JSON ✅
- [ ] ✅ Frontend otwarty: `index.html`
- [ ] ✅ Test audytu: `https://example.com` → Wyniki ✅

**Wszystko ✅? GRATULACJE! Aplikacja działa!** 🎉

---

## 🚀 ROZPOCZNIJ TERAZ!

### Pierwszy krok:

```bash
pip install -r requirements.txt
```

### Następne kroki:
1. Skonfiguruj Google API (5 min)
2. Uruchom `python app.py`
3. Otwórz `index.html`
4. Testuj!

---

**🎉 Powodzenia z audytami SEO!**

*Stworzone z Claude Code | https://claude.com/claude-code*
