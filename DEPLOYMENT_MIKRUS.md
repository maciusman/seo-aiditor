# 🚀 Deployment SEO AIditor na Mikr.us VPS

**Kompletny przewodnik deployment krok po kroku dla totalnych początkujących**

---

## 📋 Spis treści

1. [Informacje wstępne](#informacje-wstępne)
2. [Faza 1: Instalacja narzędzi](#faza-1-instalacja-narzędzi)
3. [Faza 2: Pobieranie aplikacji](#faza-2-pobieranie-aplikacji)
4. [Faza 3: Virtual Environment](#faza-3-virtual-environment)
5. [Faza 4: Konfiguracja WSGI](#faza-4-konfiguracja-wsgi)
6. [Faza 5: Test ręczny](#faza-5-test-ręczny)
7. [Faza 6: Systemd Service](#faza-6-systemd-service)
8. [Faza 7: Konfiguracja subdomeny](#faza-7-konfiguracja-subdomeny)
9. [Faza 8: Testowanie produkcyjne](#faza-8-testowanie-produkcyjne)
10. [FAQ](#faq)
11. [Maintenance](#maintenance)
12. [Troubleshooting](#troubleshooting)

---

## Informacje wstępne

### ✅ Co masz przygotowane:

- **Mikr.us VPS:** Mikrus 2.1 (1GB RAM, 10GB dysk)
- **System:** Ubuntu 24.04.3 LTS
- **Python:** 3.12.3 (najnowszy!)
- **Git:** 2.43.0
- **Subdomena:** `seoaiditor.tojest.dev` (już utworzona)
- **SSH:** Dostęp do konsoli

### 🎯 Co osiągniemy:

- ✅ Działająca aplikacja SEO AIditor na `https://seoaiditor.tojest.dev`
- ✅ Automatyczne SSL/HTTPS (dzięki Mikr.us subdomain)
- ✅ Auto-start przy reboot (systemd service)
- ✅ Inline panel API keys (bez problemów z modal)
- ✅ Pełna izolacja dependencies (virtual environment)

### ⏱️ Szacowany czas:

**40-45 minut** (spokojnie, krok po kroku)

### 📦 Architektura:

```
Internet
    ↓
https://seoaiditor.tojest.dev (Mikr.us reverse proxy + SSL)
    ↓
Port 5000 → Gunicorn (systemd service)
    ↓
Flask App (app.py) → Audyt SEO
```

---

## Faza 1: Instalacja narzędzi

### 📋 Co robimy:
Instalujemy `pip3` (instalator pakietów Python) i `python3-venv` (do tworzenia wirtualnych środowisk).

### 💡 Dlaczego:
- **pip3** jest potrzebny do instalacji Flask, Gunicorn, Requests itp.
- **venv** izoluje dependencies naszej aplikacji od systemu (bezpieczeństwo)

### 🔧 Wykonaj:

#### Krok 1.1: Update systemu

Skopiuj tę komendę:
```bash
sudo apt update
```

**Wklej do terminala** (prawy przycisk myszy → Paste) i naciśnij **Enter**.

**Co zobaczysz:**
```
Hit:1 http://archive.ubuntu.com/ubuntu noble InRelease
Get:2 http://security.ubuntu.com/ubuntu noble-security InRelease
Reading package lists... Done
Building dependency tree... Done
```

✅ **Poczekaj** aż komenda się zakończy (wrócisz do znaku `➜ ~`)

---

#### Krok 1.2: Instalacja pip3 i venv

Skopiuj:
```bash
sudo apt install -y python3-pip python3-venv
```

Naciśnij **Enter**.

**Co zobaczysz:**
```
Reading package lists... Done
Building dependency tree... Done
The following NEW packages will be installed:
  python3-pip python3-venv
...
Setting up python3-pip...
Setting up python3-venv...
```

✅ **Poczekaj** ~30-60 sekund aż instalacja się zakończy.

---

#### Krok 1.3: Weryfikacja

Sprawdź czy pip3 zainstalował się:
```bash
pip3 --version
```

**Powinno pokazać:**
```
pip 24.0 from /usr/lib/python3/dist-packages/pip (python 3.12)
```

✅ **Jeśli widzisz wersję pip → sukces!**

⚠️ **Jeśli nadal "command not found":**
- Spróbuj: `python3 -m pip --version`
- Jeśli działa → użyj `python3 -m pip` zamiast `pip3` w kolejnych krokach

---

## Faza 2: Pobieranie aplikacji

### 📋 Co robimy:
Pobieramy kod SEO AIditor z GitHub do folderu `/var/www/seoaiditor`.

### 💡 Dlaczego:
- `/var/www/` to standardowa lokalizacja dla aplikacji webowych
- Pobieramy najnowszą wersję z inline API panel (bez problemów z modal)

### 🔧 Wykonaj:

#### Krok 2.1: Przejdź do folderu /var/www

```bash
cd /var/www
```

⚠️ **Jeśli zobaczysz błąd:**
```
cd: no such file or directory: /var/www
```

**Rozwiązanie:** Utwórz folder:
```bash
sudo mkdir -p /var/www
cd /var/www
```

---

#### Krok 2.2: Sklonuj repozytorium

```bash
sudo git clone https://github.com/maciusman/seo-aiditor.git
```

**Co zobaczysz:**
```
Cloning into 'seo-aiditor'...
remote: Enumerating objects: 1234, done.
remote: Counting objects: 100% (1234/1234), done.
remote: Compressing objects: 100% (789/789), done.
Receiving objects: 100% (1234/1234), 2.45 MiB | 8.32 MiB/s, done.
Resolving deltas: 100% (567/567), done.
```

✅ **Poczekaj** aż pobierze wszystkie pliki (~10-20 sekund).

---

#### Krok 2.3: Wejdź do folderu aplikacji

```bash
cd seo-aiditor
```

---

#### Krok 2.4: Sprawdź pliki

```bash
ls -la
```

**Powinno pokazać:**
```
total 156
drwxr-xr-x  6 root root  4096 Oct  3 18:00 .
drwxr-xr-x  3 root root  4096 Oct  3 18:00 ..
-rw-r--r--  1 root root  1234 Oct  3 18:00 app.py
-rw-r--r--  1 root root  5678 Oct  3 18:00 audit_engine.py
-rw-r--r--  1 root root  2345 Oct  3 18:00 config.py
-rw-r--r--  1 root root 98765 Oct  3 18:00 index.html
-rw-r--r--  1 root root   234 Oct  3 18:00 requirements.txt
...
```

✅ **Jeśli widzisz pliki jak** `app.py`, `requirements.txt`, `index.html` → sukces!

---

## Faza 3: Virtual Environment

### 📋 Co robimy:
Tworzymy izolowane środowisko Python i instalujemy wszystkie wymagane pakiety.

### 💡 Dlaczego:
- **Virtual environment** = sandbox dla aplikacji (nie psuje systemowego Pythona)
- Instalujemy: Flask, Gunicorn, Requests, BeautifulSoup, Google Gemini API itp.

### 🔧 Wykonaj:

#### Krok 3.1: Utwórz virtual environment

Upewnij się że jesteś w `/var/www/seo-aiditor`:
```bash
pwd
```

**Powinno pokazać:**
```
/var/www/seo-aiditor
```

Teraz utwórz venv:
```bash
python3 -m venv venv
```

**Co zobaczysz:**
Nic specjalnego - komenda pracuje ~10 sekund i wraca do znaku `➜`.

✅ **Sprawdź czy folder venv powstał:**
```bash
ls -la | grep venv
```

**Powinno pokazać:**
```
drwxr-xr-x  5 root root  4096 Oct  3 18:05 venv
```

---

#### Krok 3.2: Aktywuj virtual environment

```bash
source venv/bin/activate
```

**Co zobaczysz:**
Znak przed komendą zmieni się na:
```
(venv) ➜  seo-aiditor
```

✅ **`(venv)` przed znakiem → venv jest aktywny!**

**💡 Wyjaśnienie:**
- Teraz wszystkie komendy `pip` będą instalować pakiety **TYLKO** w tym venv
- Systemowy Python jest bezpieczny

---

#### Krok 3.3: Upgrade pip (opcjonalne, ale polecane)

```bash
pip install --upgrade pip
```

**Co zobaczysz:**
```
Requirement already satisfied: pip in ./venv/lib/python3.12/site-packages
Collecting pip
  Downloading pip-24.3.1-py3-none-any.whl (1.8 MB)
Installing collected packages: pip
Successfully installed pip-24.3.1
```

---

#### Krok 3.4: Instaluj dependencies z requirements.txt

```bash
pip install -r requirements.txt
```

**Co zobaczysz:**
```
Collecting Flask>=3.0.0
  Downloading Flask-3.0.3-py3-none-any.whl (101 kB)
Collecting flask-cors>=4.0.0
  Downloading Flask_Cors-4.0.2-py2.py3-none-any.whl (14 kB)
Collecting requests>=2.31.0
  Downloading requests-2.31.0-py3-none-any.whl (62 kB)
...
Installing collected packages: Flask, flask-cors, requests, beautifulsoup4, textstat, validators, google-genai, gunicorn
Successfully installed Flask-3.0.3 flask-cors-4.0.2 requests-2.31.0 ...
```

✅ **Poczekaj** ~1-2 minuty aż wszystkie pakiety się zainstalują.

⚠️ **Jeśli zobaczysz błędy:**
- Czerwone linie z "ERROR" → skopiuj błąd i sprawdź w sekcji [Troubleshooting](#troubleshooting)
- Żółte linie z "WARNING" → można zignorować

---

#### Krok 3.5: Weryfikacja instalacji

Sprawdź czy Gunicorn zainstalował się:
```bash
which gunicorn
```

**Powinno pokazać:**
```
/var/www/seo-aiditor/venv/bin/gunicorn
```

✅ **Jeśli widzisz ścieżkę → instalacja OK!**

---

## Faza 4: Konfiguracja WSGI

### 📋 Co robimy:
Tworzymy plik `wsgi.py` - entry point dla Gunicorn.

### 💡 Dlaczego:
- Gunicorn potrzebuje `wsgi.py` żeby wiedzieć jak uruchomić Flask
- Ustawiamy `PRODUCTION=true` → aplikacja wymusza API keys od użytkowników

### 🔧 Wykonaj:

#### Krok 4.1: Utwórz plik wsgi.py

Użyjemy edytora `nano` (prosty edytor tekstowy w terminalu):

```bash
nano wsgi.py
```

**Co zobaczysz:**
Otworzy się edytor - pusty ekran z paskiem na dole.

---

#### Krok 4.2: Wklej kod

**Skopiuj dokładnie ten kod:**

```python
import sys
import os

# Dodaj ścieżkę do aplikacji
path = '/var/www/seo-aiditor'
if path not in sys.path:
    sys.path.append(path)

# Ustaw tryb produkcyjny
os.environ['PRODUCTION'] = 'true'

# Importuj aplikację Flask
from app import app as application

if __name__ == "__main__":
    application.run()
```

**Wklej do edytora nano** (prawy przycisk myszy → Paste).

---

#### Krok 4.3: Zapisz plik

1. Naciśnij **Ctrl + O** (zapisz)
2. Naciśnij **Enter** (potwierdź nazwę pliku `wsgi.py`)
3. Naciśnij **Ctrl + X** (wyjdź z nano)

✅ **Wrócisz do terminala.**

---

#### Krok 4.4: Sprawdź czy plik powstał

```bash
cat wsgi.py
```

**Powinno pokazać kod** który wkleiłeś.

✅ **Jeśli widzisz kod → sukces!**

---

## Faza 5: Test ręczny

### 📋 Co robimy:
Uruchamiamy Gunicorn ręcznie na porcie 5000 i testujemy czy aplikacja działa.

### 💡 Dlaczego:
- Lepiej najpierw przetestować ręcznie zanim zrobimy systemd service
- Jeśli coś nie działa → łatwiej debugować

### 🔧 Wykonaj:

#### Krok 5.1: Upewnij się że venv jest aktywny

Sprawdź czy widzisz `(venv)` przed znakiem:
```
(venv) ➜  seo-aiditor
```

⚠️ **Jeśli nie ma `(venv)`:**
```bash
source venv/bin/activate
```

---

#### Krok 5.2: Uruchom Gunicorn

```bash
gunicorn --bind 0.0.0.0:5000 wsgi:app
```

**Co zobaczysz:**
```
[2025-10-03 18:15:32 +0000] [12345] [INFO] Starting gunicorn 21.2.0
[2025-10-03 18:15:32 +0000] [12345] [INFO] Listening at: http://0.0.0.0:5000 (12345)
[2025-10-03 18:15:32 +0000] [12345] [INFO] Using worker: sync
[2025-10-03 18:15:32 +0000] [12346] [INFO] Booting worker with pid: 12346
```

✅ **"Listening at: http://0.0.0.0:5000"** → Gunicorn działa!

---

#### Krok 5.3: Test w przeglądarce

**NIE ZAMYKAJ TERMINALA!** Gunicorn musi działać w tle.

1. **Otwórz nową kartę** w przeglądarce
2. Wejdź na: **`http://seoaiditor.tojest.dev`** (bez https na razie)
3. **Albo:** `https://seoaiditor.tojest.dev` (z SSL przez Mikr.us)

**Co powinieneś zobaczyć:**
- ✅ Stronę SEO AIditor
- ✅ Żółty panel "🔑 API Keys Required"
- ✅ Logo, URL input, przycisk "Uruchom audyt"

⚠️ **Jeśli widzisz błąd:**
- "502 Bad Gateway" → sprawdź czy Gunicorn nadal działa w terminalu
- "Connection refused" → sprawdź czy subdomena wskazuje na port 5000
- Inna strona → sprawdź czy subdomena jest poprawnie skonfigurowana

✅ **Jeśli widzisz stronę SEO AIditor → DZIAŁA!**

---

#### Krok 5.4: Zatrzymaj Gunicorn

**Wróć do terminala** gdzie Gunicorn działa.

Naciśnij **Ctrl + C** (zatrzymaj Gunicorn).

**Co zobaczysz:**
```
^C[2025-10-03 18:20:15 +0000] [12345] [INFO] Handling signal: int
[2025-10-03 18:20:15 +0000] [12346] [INFO] Worker exiting (pid: 12346)
[2025-10-03 18:20:15 +0000] [12345] [INFO] Shutting down: Master
```

✅ **Gunicorn zatrzymany.** Teraz zrobimy systemd service żeby działał w tle zawsze.

---

## Faza 6: Systemd Service

### 📋 Co robimy:
Tworzymy systemd service - Gunicorn będzie działał w tle i uruchamiał się automatycznie przy reboot.

### 💡 Dlaczego:
- Bez tego aplikacja wyłączy się jak zamkniesz terminal
- Systemd uruchomi aplikację po restarcie serwera
- Auto-restart jeśli aplikacja się wywali

### 🔧 Wykonaj:

#### Krok 6.1: Deaktywuj venv (przed sudo)

```bash
deactivate
```

**Znak zmieni się z:**
```
(venv) ➜  seo-aiditor
```

**Na:**
```
➜  seo-aiditor
```

---

#### Krok 6.2: Utwórz plik systemd service

```bash
sudo nano /etc/systemd/system/seoaiditor.service
```

**Otworzy się edytor nano.**

---

#### Krok 6.3: Wklej konfigurację

**Skopiuj dokładnie ten kod:**

```ini
[Unit]
Description=SEO AIditor - Gunicorn WSGI server
After=network.target

[Service]
User=root
Group=root
WorkingDirectory=/var/www/seo-aiditor
Environment="PATH=/var/www/seo-aiditor/venv/bin"
Environment="PRODUCTION=true"
ExecStart=/var/www/seo-aiditor/venv/bin/gunicorn --workers 3 --bind 0.0.0.0:5000 wsgi:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Wklej do nano.**

---

#### Krok 6.4: Zapisz i wyjdź

1. **Ctrl + O** → Enter (zapisz)
2. **Ctrl + X** (wyjdź)

---

#### Krok 6.5: Przeładuj systemd

```bash
sudo systemctl daemon-reload
```

**Nie pokaże nic** - to normalne.

---

#### Krok 6.6: Włącz auto-start

```bash
sudo systemctl enable seoaiditor
```

**Co zobaczysz:**
```
Created symlink /etc/systemd/system/multi-user.target.wants/seoaiditor.service → /etc/systemd/system/seoaiditor.service.
```

✅ **Symlink utworzony → auto-start włączony!**

---

#### Krok 6.7: Uruchom service

```bash
sudo systemctl start seoaiditor
```

**Nie pokaże nic** - to normalne.

---

#### Krok 6.8: Sprawdź status

```bash
sudo systemctl status seoaiditor
```

**Co powinieneś zobaczyć:**
```
● seoaiditor.service - SEO AIditor - Gunicorn WSGI server
     Loaded: loaded (/etc/systemd/system/seoaiditor.service; enabled; preset: enabled)
     Active: active (running) since Thu 2025-10-03 18:25:00 UTC; 5s ago
   Main PID: 23456 (gunicorn)
      Tasks: 4 (limit: 1131)
     Memory: 78.5M (peak: 82.1M)
        CPU: 1.234s
     CGroup: /system.slice/seoaiditor.service
             ├─23456 /var/www/seo-aiditor/venv/bin/python3 /var/www/seo-aiditor/venv/bin/gunicorn --workers 3 --bind 0.0.0.0:5000 wsgi:app
             ├─23457 /var/www/seo-aiditor/venv/bin/python3 /var/www/seo-aiditor/venv/bin/gunicorn --workers 3 --bind 0.0.0.0:5000 wsgi:app
             ├─23458 /var/www/seo-aiditor/venv/bin/python3 /var/www/seo-aiditor/venv/bin/gunicorn --workers 3 --bind 0.0.0.0:5000 wsgi:app
             └─23459 /var/www/seo-aiditor/venv/bin/python3 /var/www/seo-aiditor/venv/bin/gunicorn --workers 3 --bind 0.0.0.0:5000 wsgi:app

Oct 03 18:25:00 srv42 systemd[1]: Started seoaiditor.service - SEO AIditor - Gunicorn WSGI server.
Oct 03 18:25:00 srv42 gunicorn[23456]: [2025-10-03 18:25:00 +0000] [23456] [INFO] Starting gunicorn 21.2.0
Oct 03 18:25:00 srv42 gunicorn[23456]: [2025-10-03 18:25:00 +0000] [23456] [INFO] Listening at: http://0.0.0.0:5000 (23456)
Oct 03 18:25:00 srv42 gunicorn[23456]: [2025-10-03 18:25:00 +0000] [23456] [INFO] Using worker: sync
Oct 03 18:25:00 srv42 gunicorn[23457]: [2025-10-03 18:25:00 +0000] [23457] [INFO] Booting worker with pid: 23457
Oct 03 18:25:00 srv42 gunicorn[23458]: [2025-10-03 18:25:00 +0000] [23458] [INFO] Booting worker with pid: 23458
Oct 03 18:25:00 srv42 gunicorn[23459]: [2025-10-03 18:25:00 +0000] [23459] [INFO] Booting worker with pid: 23459
```

✅ **Kluczowe linie:**
- **`Active: active (running)`** → Service działa!
- **`Listening at: http://0.0.0.0:5000`** → Gunicorn słucha na porcie 5000!
- **`enabled`** → Auto-start włączony!

⚠️ **Jeśli widzisz `Active: failed`:**
- Sprawdź logi: `sudo journalctl -u seoaiditor -n 50`
- Skopiuj błąd i sprawdź w [Troubleshooting](#troubleshooting)

---

#### Krok 6.9: Wyjdź ze statusu

Naciśnij **Q** (quit).

---

## Faza 7: Konfiguracja subdomeny

### 📋 Co masz już zrobione:

✅ **Subdomena utworzona:** `seoaiditor.tojest.dev`
✅ **Port:** 5000
✅ **Mikr.us robi automatycznie:**
- Reverse proxy (ruch z internetu → Twój port 5000)
- SSL/HTTPS (darmowy certyfikat)
- Routing

### 💡 Weryfikacja w panelu Mikr.us:

1. Zaloguj się: **https://mikr.us/panel/**
2. Kliknij **"Subdomeny"**
3. Sprawdź czy widzisz:

```
Subdomena: seoaiditor.tojest.dev
Port: 5000
Status: ✅ (zielony ptaszek)
```

✅ **Jeśli widzisz zielony ptaszek → subdomena działa!**

⚠️ **Jeśli widzisz żółty znak lub błąd:**
- Poczekaj 2-5 minut (propagacja DNS)
- Odśwież stronę panelu
- Sprawdź czy port 5000 jest otwarty: `sudo netstat -tlnp | grep 5000`

---

## Faza 8: Testowanie produkcyjne

### 📋 Co robimy:
Testujemy aplikację w trybie produkcyjnym z prawdziwymi API keys.

### 🔧 Wykonaj:

#### Krok 8.1: Otwórz aplikację w przeglądarce

Wejdź na: **`https://seoaiditor.tojest.dev`**

**Co powinieneś zobaczyć:**

1. ✅ **Żółty panel API Keys:**
   - Gradient: żółty (#fef3c7 → #fde68a)
   - Tekst: "🔑 API Keys Required"
   - Przycisk: "▼ Configure"

2. ✅ **Header z logo:** "SEO AIditor - Profesjonalne Narzędzie do Audytu SEO"

3. ✅ **URL Input:** "Wprowadź URL strony do audytu"

4. ✅ **Przycisk:** "Uruchom audyt"

---

#### Krok 8.2: Rozwiń panel API Keys

1. Kliknij przycisk **"▼ Configure"**
2. Panel się rozwinie

**Co powinieneś zobaczyć:**

- **Input 1:** "🤖 Google Gemini API Key *"
  - Placeholder: "AIzaSy..."
  - Przycisk: 👁️ (show/hide)
  - Link: "→ Get free key (2 min)"

- **Input 2:** "⚡ PageSpeed Insights API Key (optional)"
  - Placeholder: "AIzaSy... (optional)"
  - Przycisk: 👁️ (show/hide)
  - Link: "→ Get free key (optional)"

- **Checkbox:** "Remember keys (saved in browser storage)"

- **Przycisk:** "💾 Save & Continue"

---

#### Krok 8.3: Wprowadź API keys

**Jeśli masz klucze API:**

1. **Gemini API key:** Wklej do pierwszego inputa
2. **PSI API key (opcjonalnie):** Wklej do drugiego inputa
3. **Zaznacz checkbox** "Remember keys" (jeśli chcesz zapamiętać)
4. Kliknij **"💾 Save & Continue"**

**Panel powinien się zwinąć i zmienić kolor na ZIELONY:**
- Gradient: zielony (#d1fae5 → #a7f3d0)
- Tekst: "🔑 API Keys Configured ✓"
- Przycisk: "▼ Edit Keys"

✅ **Zielony panel = klucze zapisane!**

---

**Jeśli NIE masz kluczy API:**

1. Kliknij link **"→ Get free key (2 min)"** przy Gemini
2. Otworzy się: https://aistudio.google.com/apikey
3. Zaloguj się na konto Google
4. Kliknij **"Create API key"**
5. Skopiuj klucz (zaczyna się od `AIzaSy...`)
6. Wklej do aplikacji
7. Kliknij **"💾 Save & Continue"**

**PSI key (opcjonalny):**
- Jeśli chcesz pełne dane Performance → pobierz również PSI key
- Jeśli nie → zostaw puste (będą podstawowe metryki)

---

#### Krok 8.4: Uruchom testowy audyt

1. **Wpisz URL:** `https://example.com` (lub dowolną stronę)
2. Kliknij **"Uruchom audyt"**

**Co powinieneś zobaczyć:**

1. **Pasek postępu:**
   ```
   Analizuję... 45%
   ⏳ Pobieranie strony...
   ```

2. **Po ~10-30 sekundach:**
   - ✅ Wyniki audytu (5 zakładek: Overview, Technical, On-Page, Content, Performance)
   - ✅ Ogólny wynik (0-100)
   - ✅ Quick Wins
   - ✅ AI Recommendations

3. **Przyciski eksportu:**
   - "📄 Eksportuj do CSV"
   - "📋 Eksportuj do HTML"

---

#### Krok 8.5: Weryfikacja błędów

⚠️ **Jeśli zobaczysz błąd:**

**Błąd: "Cannot fetch page"**
- ✅ To już NIE powinno się zdarzać (Mikr.us VPS nie ma whitelist)
- ❌ Jeśli jednak widzisz → sprawdź logi: `sudo journalctl -u seoaiditor -n 50`

**Błąd: "Gemini API key is required"**
- ❌ Panel nie zapisał kluczy → odśwież stronę i wprowadź ponownie

**Błąd: "Invalid API key"**
- ❌ Klucz nieprawidłowy → sprawdź czy skopiowałeś pełny klucz (zaczyna się `AIzaSy...`)

**Błąd sieciowy:**
- ❌ Aplikacja nie działa → sprawdź status: `sudo systemctl status seoaiditor`

---

✅ **Jeśli audyt działa BEZ błędów:**

**GRATULACJE!** 🎉

Aplikacja SEO AIditor działa w trybie produkcyjnym na:
**`https://seoaiditor.tojest.dev`**

---

## FAQ

### ❓ Jak sprawdzić logi aplikacji?

```bash
sudo journalctl -u seoaiditor -f
```

Naciśnij **Ctrl + C** żeby zakończyć.

---

### ❓ Jak zrestartować aplikację?

```bash
sudo systemctl restart seoaiditor
```

---

### ❓ Jak zaktualizować kod z GitHub?

```bash
cd /var/www/seo-aiditor
sudo git pull origin master
sudo systemctl restart seoaiditor
```

---

### ❓ Jak zatrzymać aplikację?

```bash
sudo systemctl stop seoaiditor
```

**Uruchom ponownie:**
```bash
sudo systemctl start seoaiditor
```

---

### ❓ Co jeśli subdomena nie działa?

1. Sprawdź w panelu Mikr.us: https://mikr.us/panel/ → Subdomeny
2. Sprawdź status: Zielony ptaszek ✅ = działa
3. Sprawdź port: Powinien być 5000
4. Odśwież stronę panelu i poczekaj 2-5 minut

---

### ❓ Jak sprawdzić czy Gunicorn działa?

```bash
sudo systemctl status seoaiditor
```

Szukaj: `Active: active (running)` i `Listening at: http://0.0.0.0:5000`

---

### ❓ Jak zmienić liczbę workers Gunicorn?

Edytuj service:
```bash
sudo nano /etc/systemd/system/seoaiditor.service
```

Zmień linię:
```
ExecStart=/var/www/seo-aiditor/venv/bin/gunicorn --workers 3 --bind 0.0.0.0:5000 wsgi:app
```

**Rekomendacja workers:** `(2 x CPU cores) + 1`
- Mikrus 2.1 ma ~2 vCPU → 5 workers max
- Default: 3 workers (bezpieczne)

Zapisz (Ctrl+O, Enter, Ctrl+X) i zrestartuj:
```bash
sudo systemctl daemon-reload
sudo systemctl restart seoaiditor
```

---

### ❓ Jak dodać monitoring?

Zainstaluj `htop`:
```bash
sudo apt install -y htop
```

Uruchom:
```bash
htop
```

Zobaczysz:
- CPU usage
- RAM usage
- Procesy Python/Gunicorn

Naciśnij **Q** żeby wyjść.

---

## Maintenance

Zobacz pełny przewodnik: [MAINTENANCE_MIKRUS.md](MAINTENANCE_MIKRUS.md)

**Podstawowe zadania:**

### 📊 Sprawdzanie statusu (codziennie)

```bash
sudo systemctl status seoaiditor
```

---

### 🔄 Aktualizacja aplikacji (gdy są zmiany w GitHub)

```bash
cd /var/www/seo-aiditor
sudo git pull origin master
sudo systemctl restart seoaiditor
```

---

### 📝 Sprawdzanie logów (gdy coś nie działa)

**Ostatnie 50 linii:**
```bash
sudo journalctl -u seoaiditor -n 50
```

**Live monitoring:**
```bash
sudo journalctl -u seoaiditor -f
```

---

### 💾 Backup aplikacji (raz w miesiącu)

```bash
cd /var/www
sudo tar -czf seoaiditor-backup-$(date +%Y%m%d).tar.gz seo-aiditor/
```

**Lista backupów:**
```bash
ls -lh /var/www/*.tar.gz
```

---

### 🔐 Update systemu (raz w tygodniu)

```bash
sudo apt update && sudo apt upgrade -y
```

**Restart jeśli kernel update:**
```bash
sudo reboot
```

(Aplikacja auto-startuje po reboot dzięki systemd!)

---

## Troubleshooting

Zobacz pełny przewodnik: [TROUBLESHOOTING_MIKRUS.md](TROUBLESHOOTING_MIKRUS.md)

### ⚠️ Problem: "Active: failed" w systemctl status

**Diagnoza:**
```bash
sudo journalctl -u seoaiditor -n 50
```

**Najczęstsze przyczyny:**

1. **Import error (brak modułu):**
   ```
   ModuleNotFoundError: No module named 'flask'
   ```

   **Rozwiązanie:**
   ```bash
   cd /var/www/seo-aiditor
   source venv/bin/activate
   pip install -r requirements.txt
   deactivate
   sudo systemctl restart seoaiditor
   ```

2. **Port zajęty:**
   ```
   [ERROR] Connection in use: ('0.0.0.0', 5000)
   ```

   **Rozwiązanie:**
   ```bash
   sudo lsof -ti:5000 | sudo xargs kill -9
   sudo systemctl restart seoaiditor
   ```

3. **Błąd w wsgi.py:**
   ```
   Failed to find application object 'app' in 'wsgi'
   ```

   **Rozwiązanie:**
   ```bash
   cd /var/www/seo-aiditor
   cat wsgi.py
   ```

   Upewnij się że ostatnia linia to:
   ```python
   from app import app as application
   ```

---

### ⚠️ Problem: Subdomena pokazuje "502 Bad Gateway"

**Diagnoza:**
1. Sprawdź czy Gunicorn działa:
   ```bash
   sudo systemctl status seoaiditor
   ```

2. Sprawdź czy port 5000 jest otwarty:
   ```bash
   sudo netstat -tlnp | grep 5000
   ```

**Rozwiązanie:**
```bash
sudo systemctl restart seoaiditor
```

Poczekaj 10 sekund i odśwież przeglądarkę.

---

### ⚠️ Problem: "Cannot fetch page" przy audycie

**To już NIE powinno się zdarzać na Mikr.us VPS!**

**Jeśli jednak widzisz:**

1. Sprawdź logi backendu:
   ```bash
   sudo journalctl -u seoaiditor -f
   ```

2. Uruchom testowy request:
   ```bash
   curl https://example.com
   ```

3. Jeśli `curl` działa → problem w kodzie aplikacji
4. Jeśli `curl` nie działa → problem z DNS/network na serwerze

---

### ⚠️ Problem: Panel API keys nie zapisuje kluczy

**Przyczyna:** LocalStorage/SessionStorage zablokowany w przeglądarce

**Rozwiązanie:**
1. Otwórz DevTools (F12)
2. Console → sprawdź błędy
3. Sprawdź czy widzisz: "localStorage is not defined"
4. Wyłącz tryb prywatny / włącz cookies dla domeny

---

### ⚠️ Problem: Aplikacja działa ale jest wolna

**Diagnoza:**
```bash
htop
```

Sprawdź:
- **CPU usage:** Powinien być < 70%
- **RAM usage:** Powinien być < 800MB (z 1GB)

**Rozwiązanie - zwiększ workers:**
```bash
sudo nano /etc/systemd/system/seoaiditor.service
```

Zmień `--workers 3` na `--workers 5`.

Zapisz, przeładuj:
```bash
sudo systemctl daemon-reload
sudo systemctl restart seoaiditor
```

---

### ⚠️ Problem: Po reboot aplikacja nie startuje

**Diagnoza:**
```bash
sudo systemctl is-enabled seoaiditor
```

**Powinno pokazać:** `enabled`

**Jeśli pokazuje `disabled`:**
```bash
sudo systemctl enable seoaiditor
sudo systemctl start seoaiditor
```

---

## 🎉 Podsumowanie

**Co osiągnąłeś:**

✅ **Działająca aplikacja:** `https://seoaiditor.tojest.dev`
✅ **Auto-start:** Systemd service uruchamia się przy reboot
✅ **SSL/HTTPS:** Darmowy certyfikat przez Mikr.us subdomain
✅ **Inline API panel:** Bez problemów z modal/endpoint
✅ **Izolacja:** Virtual environment (nie psuje systemu)
✅ **Monitoring:** Logi przez journalctl
✅ **Maintenance:** Proste komendy update/restart

---

## 📚 Dodatkowe zasoby

- **Maintenance:** [MAINTENANCE_MIKRUS.md](MAINTENANCE_MIKRUS.md)
- **Troubleshooting:** [TROUBLESHOOTING_MIKRUS.md](TROUBLESHOOTING_MIKRUS.md)
- **Mikr.us Wiki:** https://wiki.mikr.us/
- **Gunicorn Docs:** https://docs.gunicorn.org/
- **Flask Deployment:** https://flask.palletsprojects.com/en/stable/deploying/

---

## ❓ Potrzebujesz pomocy?

**Jeśli coś nie działa:**

1. Sprawdź [Troubleshooting](#troubleshooting)
2. Sprawdź logi: `sudo journalctl -u seoaiditor -n 50`
3. Sprawdź status: `sudo systemctl status seoaiditor`
4. Wróć do tego README i szukaj sekcji FAQ

**Jeśli nadal problem:**
- Skopiuj **dokładny błąd** z logów
- Opisz **co robiłeś** przed błędem
- Sprawdź **GitHub Issues:** https://github.com/maciusman/seo-aiditor/issues

---

**Powodzenia! 🚀**

Masz teraz profesjonalną aplikację SEO AIditor działającą w chmurze!
