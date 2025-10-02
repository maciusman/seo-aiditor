# 🔧 Naprawa błędu 403 - Google PageSpeed API

## ❌ Błąd który widzisz:

```
Error: 403 Client Error: Forbidden for url: https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=
```

---

## ✅ ROZWIĄZANIE (3 minuty)

### Krok 1: Przejdź do Google Cloud Console

https://console.cloud.google.com/apis/credentials

### Krok 2: Znajdź swój API Key

- W sekcji "API Keys" zobaczysz swój klucz
- Kliknij na nazwę klucza (NIE kopiuj, tylko kliknij w nazwę)

### Krok 3: Usuń restrykcje API

**To jest KLUCZOWE:**

1. Znajdź sekcję **"API restrictions"**
2. Sprawdź co jest wybrane:

**OPCJA A - Jeśli wybrane "Restrict key":**
- Kliknij **"Don't restrict key"** (brak restrykcji)
- Kliknij **"SAVE"** na dole strony
- ✅ **To powinno naprawić problem!**

**OPCJA B - Jeśli chcesz zachować restrykcje (bezpieczniejsze):**
- Zostaw **"Restrict key"**
- W liście API upewnij się że jest zaznaczone: **"PageSpeed Insights API"**
- Kliknij **"SAVE"**

### Krok 4: Poczekaj 2-3 minuty

- Google potrzebuje chwilę aby zaktualizować uprawnienia
- Zrób sobie kawę ☕

### Krok 5: Testuj ponownie

```bash
# Uruchom ponownie backend:
python app.py

# Otwórz frontend i spróbuj audytu
```

---

## 🎯 Dodatkowe sprawdzenia

### Sprawdź czy PageSpeed Insights API jest WŁĄCZONE:

1. Idź do: https://console.cloud.google.com/apis/library
2. Wyszukaj: `PageSpeed Insights API`
3. Jeśli widzisz przycisk **"ENABLE"** → Kliknij go!
4. Jeśli widzisz **"MANAGE"** → Jest włączone ✅

---

## 🔍 Diagnostyka

### Test 1: Sprawdź API key bez restrykcji

Otwórz w przeglądarce (wstaw swój klucz):

```
https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=https://example.com&key=TWOJ_API_KEY
```

**Jeśli działa:** Zobaczysz JSON z wynikami ✅
**Jeśli 403:** API key ma restrykcje lub nie jest aktywny ❌

### Test 2: Sprawdź bez API key (ograniczony limit)

```
https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=https://example.com
```

**Jeśli działa:** API Google PageSpeed działa, problem jest z kluczem
**Jeśli nie działa:** Problem z połączeniem internetowym

---

## 💡 Alternatywne rozwiązanie - Użyj aplikacji BEZ API key

Aplikacja działa również **bez Google API key**, ale:
- ❌ Brak analizy Core Web Vitals (LCP, FID, CLS)
- ❌ Brak wydajności (Performance score)
- ✅ Reszta audytu SEO działa normalnie!

**Jak używać bez API key:**

1. Otwórz `config.py`
2. Zostaw:
   ```python
   GOOGLE_PSI_API_KEY = "YOUR_API_KEY_HERE"
   ```
3. Uruchom aplikację normalnie

**Aplikacja automatycznie pominie PageSpeed i użyje pozostałych 4 kategorii audytu.**

---

## 🔒 Dlaczego mam błąd 403?

### Możliwe przyczyny:

1. **API key ma restrykcje** (najczęstsze)
   - Rozwiązanie: Usuń restrykcje lub dodaj PageSpeed Insights API do listy

2. **PageSpeed Insights API nie jest włączone**
   - Rozwiązanie: Włącz w Google Cloud Console

3. **API key został usunięty/wygasł**
   - Rozwiązanie: Wygeneruj nowy klucz

4. **Przekroczono limit zapytań** (bardzo rzadko)
   - Limit: 25,000/dzień (dużo!)
   - Rozwiązanie: Poczekaj do północy lub stwórz nowy projekt

5. **IP jest zablokowane** (bardzo rzadko)
   - Rozwiązanie: Usuń restrykcje IP w API key settings

---

## 🆘 Nadal nie działa?

### Krok 1: Wygeneruj NOWY API key

1. https://console.cloud.google.com/apis/credentials
2. **"+ CREATE CREDENTIALS"** → **"API key"**
3. **Skopiuj nowy klucz**
4. **NIE dodawaj żadnych restrykcji** (przynajmniej na start)
5. Edytuj `config.py` → wstaw nowy klucz
6. Testuj

### Krok 2: Sprawdź projekt

1. Upewnij się że jesteś w poprawnym projekcie Google Cloud
2. Sprawdź czy PageSpeed Insights API jest włączone W TYM PROJEKCIE
3. Sprawdź czy API key należy DO TEGO PROJEKTU

### Krok 3: Sprawdź billing (bardzo rzadko potrzebne)

Google PageSpeed Insights API jest **darmowe** do 25,000 zapytań/dzień.

Ale w bardzo rzadkich przypadkach Google może wymagać dodania karty kredytowej do projektu (NIE będą pobierać opłat jeśli nie przekroczysz limitu).

**Tylko jeśli nic innego nie działa:**
1. Google Cloud Console → Billing
2. Dodaj payment method (karta)
3. Aktywuj darmowy tier

**UWAGA:** 99% użytkowników NIE musi tego robić!

---

## ✅ Checklist rozwiązania

Przejdź przez te kroki w kolejności:

- [ ] Sprawdź czy PageSpeed Insights API jest włączone
- [ ] Usuń restrykcje z API key ("Don't restrict key")
- [ ] Poczekaj 2-3 minuty
- [ ] Restartuj backend (`python app.py`)
- [ ] Testuj ponownie w aplikacji
- [ ] Jeśli nie działa → Wygeneruj nowy API key
- [ ] Jeśli nadal nie działa → Użyj aplikacji bez API key (ograniczona funkcjonalność)

---

## 🎯 Najszybsze rozwiązanie (90% przypadków):

1. **Google Cloud Console** → **APIs & Credentials**
2. **Kliknij na API key** (nazwę, nie kopiuj)
3. **API restrictions** → **"Don't restrict key"**
4. **SAVE**
5. **Poczekaj 2 minuty**
6. **Testuj!**

---

**✅ To powinno naprawić problem!**

Jeśli nadal masz błąd, otwórz Issue na GitHubie:
https://github.com/maciusman/seo-aiditor/issues

---

*Wygenerowano automatycznie przez Claude Code*
