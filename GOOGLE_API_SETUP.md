# 🔑 Instrukcja Konfiguracji Google PageSpeed Insights API

## Czas: ~5 minut | Koszt: DARMOWE

---

## Krok 1: Przejdź do Google Cloud Console

🔗 **Link:** [https://console.cloud.google.com/](https://console.cloud.google.com/)

- Zaloguj się swoim kontem Gmail
- Jeśli nie masz konta Google, utwórz je za darmo

---

## Krok 2: Utwórz Nowy Projekt

1. **Kliknij dropdown** przy logo Google Cloud (góra strony, obok "Google Cloud")
2. **Kliknij "New Project"**
3. **Nazwa projektu:** `SEO Audit Tool` (lub dowolna)
4. **Organization:** zostaw puste (jeśli nie masz organizacji)
5. **Kliknij "CREATE"**
6. **Poczekaj ~10 sekund** aż projekt się utworzy

---

## Krok 3: Włącz PageSpeed Insights API

1. **W menu bocznym** (☰ hamburger menu) kliknij:
   - **"APIs & Services"** → **"Library"**

2. **W wyszukiwarce wpisz:** `PageSpeed Insights API`

3. **Kliknij** na kartę **"PageSpeed Insights API"**

4. **Kliknij przycisk "ENABLE"** (niebieski przycisk)

5. **Poczekaj** aż API się włączy (~5 sekund)

---

## Krok 4: Wygeneruj API Key

1. **W menu bocznym** kliknij:
   - **"APIs & Services"** → **"Credentials"**

2. **Kliknij przycisk** **"+ CREATE CREDENTIALS"** (góra strony)

3. **Wybierz:** **"API key"**

4. **API key zostanie wygenerowany!**
   - Skopiuj klucz (wygląda jak: `AIzaSyD...`)
   - Zapisz go bezpiecznie

5. *(Opcjonalnie)* **Kliknij "RESTRICT KEY"** aby zabezpieczyć:
   - **API restrictions** → wybierz **"Restrict key"**
   - Zaznacz tylko: **"PageSpeed Insights API"**
   - Kliknij **"SAVE"**

---

## Krok 5: Wstaw API Key do Config

1. **Otwórz plik** `config.py` w swoim projekcie

2. **Znajdź linię:**
   ```python
   GOOGLE_PSI_API_KEY = "YOUR_API_KEY_HERE"
   ```

3. **Zastąp** `YOUR_API_KEY_HERE` swoim kluczem:
   ```python
   GOOGLE_PSI_API_KEY = "AIzaSyD...twój_klucz"
   ```

4. **Zapisz plik**

---

## ✅ Gotowe! Test API

### Uruchom test:

```bash
python audit_engine.py
```

Jeśli widzisz wyniki audytu (bez błędów "API key"), to **SUKCES!** 🎉

---

## 📊 Limity Darmowe

| Parametr | Wartość |
|----------|---------|
| **Zapytania dziennie** | 25,000 |
| **Zapytania na sekundę** | 1-2 |
| **Koszt** | **0 PLN/miesiąc** |
| **Karta kredytowa** | NIE wymagana |

### Co to oznacza?
- ~**800 audytów dziennie** (przy 30 requestów/audyt)
- Dla większości użytkowników **całkowicie wystarczające**
- Jeśli przekroczysz limit: API zwróci błąd (bez kosztów)

---

## 🔒 Bezpieczeństwo API Key

### ⚠️ NIGDY NIE:
- ❌ Nie commituj API key do GitHub (publiczne repo)
- ❌ Nie udostępniaj klucza publicznie
- ❌ Nie wklejaj do kodu frontend (JavaScript w przeglądarce)

### ✅ ZAWSZE:
- ✅ Trzymaj API key w `config.py` (backend tylko)
- ✅ Dodaj `config.py` do `.gitignore`
- ✅ Użyj environment variables w produkcji:
  ```python
  import os
  GOOGLE_PSI_API_KEY = os.environ.get('PSI_API_KEY', 'YOUR_KEY')
  ```

---

## 🐛 Troubleshooting

### Błąd: "API key not valid"
**Rozwiązanie:**
1. Sprawdź czy skopiowałeś cały klucz (bez spacji)
2. Upewnij się że PageSpeed Insights API jest ENABLED
3. Poczekaj 2-3 minuty po utworzeniu klucza (propagacja)

### Błąd: "Quota exceeded"
**Rozwiązanie:**
- Przekroczyłeś 25,000 zapytań/dzień
- Zaczekaj do północy (reset limitu)
- Lub stwórz nowy projekt z nowym API key

### Błąd: "IP address blocked"
**Rozwiązanie:**
- Usuń API restrictions
- Lub dodaj swoje IP do whitelist w Google Cloud

---

## 📚 Dodatkowe Zasoby

- [PageSpeed Insights API Docs](https://developers.google.com/speed/docs/insights/v5/get-started)
- [Google Cloud Pricing](https://cloud.google.com/apis/docs/overview#pricing) (darmowy tier)
- [API Key Best Practices](https://cloud.google.com/docs/authentication/api-keys)

---

**🚀 Gotowe do uruchomienia SEO AIditor!**

Jeśli masz problemy, sprawdź `README.md` lub otwórz issue na GitHub.
