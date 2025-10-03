# 🔧 Troubleshooting Guide - SEO AIditor na Mikr.us VPS

**Rozwiązania najczęstszych problemów**

---

## 📋 Spis treści

1. [Aplikacja nie startuje](#aplikacja-nie-startuje)
2. [Subdomena nie działa](#subdomena-nie-działa)
3. [Błędy podczas audytu](#błędy-podczas-audytu)
4. [Problemy z API keys](#problemy-z-api-keys)
5. [Problemy z wydajnością](#problemy-z-wydajnością)
6. [Błędy instalacji](#błędy-instalacji)
7. [Błędy Git](#błędy-git)
8. [Problemy z SSH](#problemy-z-ssh)

---

## Aplikacja nie startuje

### ❌ Problem: `Active: failed` w systemctl status

**Komenda diagnostyczna:**
```bash
sudo systemctl status seoaiditor
```

**Output:**
```
● seoaiditor.service - SEO AIditor - Gunicorn WSGI server
     Loaded: loaded (/etc/systemd/system/seoaiditor.service; enabled)
     Active: failed (Result: exit-code) since Thu 2025-10-03 19:45:00 UTC; 5s ago
    Process: 12345 ExecStart=/var/www/seo-aiditor/venv/bin/gunicorn --workers 3 --bind 0.0.0.0:5000 wsgi:app (code=exited, status=1/FAILURE)
```

**Sprawdź szczegółowe logi:**
```bash
sudo journalctl -u seoaiditor -n 100 --no-pager
```

---

#### Rozwiązanie 1: Import Error (brak modułu)

**Błąd w logach:**
```
ModuleNotFoundError: No module named 'flask'
ModuleNotFoundError: No module named 'requests'
```

**Rozwiązanie:**
```bash
cd /var/www/seo-aiditor
source venv/bin/activate
pip install -r requirements.txt
deactivate
sudo systemctl restart seoaiditor
```

**Weryfikacja:**
```bash
sudo systemctl status seoaiditor
```

Szukaj: `Active: active (running)`

---

#### Rozwiązanie 2: Port zajęty

**Błąd w logach:**
```
[ERROR] Connection in use: ('0.0.0.0', 5000)
[ERROR] Retrying in 1 second.
```

**Diagnoza - kto używa portu 5000:**
```bash
sudo lsof -i :5000
```

**Output:**
```
COMMAND   PID USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
python3 12345 root    3u  IPv4  67890      0t0  TCP *:5000 (LISTEN)
```

**Rozwiązanie - kill proces:**
```bash
sudo lsof -ti:5000 | sudo xargs kill -9
```

**Restart aplikacji:**
```bash
sudo systemctl restart seoaiditor
```

---

#### Rozwiązanie 3: Błąd w wsgi.py

**Błąd w logach:**
```
Failed to find application object 'app' in 'wsgi'
ImportError: cannot import name 'app' from 'wsgi'
```

**Sprawdź wsgi.py:**
```bash
cat /var/www/seo-aiditor/wsgi.py
```

**Powinno być:**
```python
from app import app as application
```

**Jeśli błąd - popraw:**
```bash
nano /var/www/seo-aiditor/wsgi.py
```

Upewnij się że ostatnia linia importu to:
```python
from app import app as application
```

Zapisz: Ctrl+O, Enter, Ctrl+X

**Restart:**
```bash
sudo systemctl restart seoaiditor
```

---

#### Rozwiązanie 4: Permission denied

**Błąd w logach:**
```
PermissionError: [Errno 13] Permission denied: '/var/www/seo-aiditor'
```

**Napraw uprawnienia:**
```bash
sudo chown -R root:root /var/www/seo-aiditor
sudo chmod -R 755 /var/www/seo-aiditor
```

**Restart:**
```bash
sudo systemctl restart seoaiditor
```

---

#### Rozwiązanie 5: Virtual environment uszkodzony

**Błąd w logach:**
```
/var/www/seo-aiditor/venv/bin/python3: No such file or directory
```

**Rozwiązanie - odtwórz venv:**
```bash
cd /var/www/seo-aiditor
sudo rm -rf venv/
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
deactivate
sudo systemctl restart seoaiditor
```

---

## Subdomena nie działa

### ❌ Problem: "502 Bad Gateway"

**Przyczyna:** Gunicorn nie działa lub subdomena niepoprawnie skonfigurowana.

**Krok 1: Sprawdź czy Gunicorn działa**
```bash
sudo systemctl status seoaiditor
```

**Jeśli `failed`:** Zobacz sekcję [Aplikacja nie startuje](#aplikacja-nie-startuje)

**Jeśli `active (running)`:** Przejdź do Kroku 2

---

**Krok 2: Sprawdź czy port 5000 słucha**
```bash
sudo netstat -tlnp | grep 5000
```

**Powinno pokazać:**
```
tcp        0      0 0.0.0.0:5000            0.0.0.0:*               LISTEN      12345/gunicorn
```

**Jeśli nic nie pokazuje:**
- Gunicorn nie działa poprawnie
- Sprawdź logi: `sudo journalctl -u seoaiditor -n 50`

---

**Krok 3: Test lokalny curl**
```bash
curl http://localhost:5000
```

**Powinno zwrócić HTML strony (index.html).**

**Jeśli błąd:**
```
curl: (7) Failed to connect to localhost port 5000: Connection refused
```

→ Gunicorn nie działa, restart: `sudo systemctl restart seoaiditor`

---

**Krok 4: Sprawdź konfigurację subdomeny w panelu Mikr.us**

1. Zaloguj: https://mikr.us/panel/
2. Kliknij **"Subdomeny"**
3. Znajdź: `seoaiditor.tojest.dev`

**Sprawdź:**
- **Port:** Musi być `5000` (NIE 80, NIE 443)
- **Status:** Zielony ptaszek ✅
- **Checkbox "HTTPS":** NIE zaznaczony (Mikr.us doda SSL automatycznie)

**Jeśli port inny niż 5000:**
- Kliknij "Edytuj"
- Zmień port na `5000`
- Zapisz
- Poczekaj 2-5 minut (propagacja DNS)

---

**Krok 5: Test zewnętrzny**
```bash
curl https://seoaiditor.tojest.dev
```

**Powinno zwrócić HTML.**

**Jeśli błąd:**
```
curl: (6) Could not resolve host: seoaiditor.tojest.dev
```

→ DNS nie propagował się, poczekaj 5 minut i spróbuj ponownie.

---

### ❌ Problem: "Connection timed out"

**Przyczyna:** Firewall blokuje port 5000.

**Sprawdź firewall:**
```bash
sudo ufw status
```

**Jeśli pokazuje `active`:**
```bash
sudo ufw allow 5000/tcp
sudo ufw reload
```

**Restart aplikacji:**
```bash
sudo systemctl restart seoaiditor
```

---

### ❌ Problem: Subdomena pokazuje starą wersję aplikacji

**Przyczyna:** Cache przeglądarki lub Mikr.us proxy.

**Rozwiązanie:**

1. **Hard refresh przeglądarki:**
   - Windows/Linux: `Ctrl + Shift + R` lub `Ctrl + F5`
   - Mac: `Cmd + Shift + R`

2. **Wyczyść cache przeglądarki:**
   - Chrome: Settings → Privacy → Clear browsing data → Cached images
   - Firefox: Settings → Privacy → Clear Data → Cached Web Content

3. **Test w trybie incognito:**
   - Chrome: `Ctrl + Shift + N`
   - Firefox: `Ctrl + Shift + P`

4. **Sprawdź timestamp plików na serwerze:**
   ```bash
   ls -la /var/www/seo-aiditor/index.html
   ```

   Sprawdź datę modyfikacji - powinna być aktualna.

---

## Błędy podczas audytu

### ❌ Problem: "Cannot fetch page"

**To już NIE powinno się zdarzać na Mikr.us VPS** (brak whitelist outbound requests).

**Jeśli jednak widzisz:**

**Krok 1: Test curl na serwerze**
```bash
curl -I https://example.com
```

**Powinno pokazać:**
```
HTTP/2 200
content-type: text/html; charset=UTF-8
```

**Jeśli błąd:**
```
curl: (6) Could not resolve host: example.com
```

→ Problem z DNS na serwerze

**Rozwiązanie DNS:**
```bash
echo "nameserver 8.8.8.8" | sudo tee /etc/resolv.conf
echo "nameserver 8.8.4.4" | sudo tee -a /etc/resolv.conf
```

---

**Krok 2: Sprawdź logi aplikacji**
```bash
sudo journalctl -u seoaiditor -f
```

Uruchom audyt w przeglądarce i obserwuj logi.

**Szukaj:**
```
[ERROR] Cannot fetch page: <błąd>
[ERROR] Timeout connecting to https://example.com
```

---

**Krok 3: Zwiększ timeout (jeśli strony wolno ładują)**

Edytuj `audit_engine.py`:
```bash
nano /var/www/seo-aiditor/audit_engine.py
```

Znajdź (Ctrl+W "timeout"):
```python
response = requests.get(url, timeout=10, ...)
```

Zmień na:
```python
response = requests.get(url, timeout=30, ...)
```

Zapisz: Ctrl+O, Enter, Ctrl+X

**Restart:**
```bash
sudo systemctl restart seoaiditor
```

---

### ❌ Problem: "Invalid API key" / "Quota exceeded"

**Błąd w aplikacji:**
```
❌ Błąd audytu: Error: Invalid API key
❌ Błąd audytu: Error: Quota exceeded (5 requests per minute)
```

**Przyczyna:** Nieprawidłowy klucz API lub przekroczony limit.

**Rozwiązanie:**

1. **Sprawdź klucz w Google AI Studio:**
   - Wejdź: https://aistudio.google.com/apikey
   - Sprawdź czy klucz istnieje i jest aktywny

2. **Wygeneruj nowy klucz:**
   - Kliknij "Create API key"
   - Skopiuj nowy klucz (zaczyna się `AIzaSy...`)
   - Wprowadź do aplikacji

3. **Sprawdź limity:**
   - Free tier Gemini: **5 requests/min**, **25 requests/day**
   - Jeśli przekroczyłeś → poczekaj 1 minutę / 24 godziny
   - Lub upgrade do paid tier: https://ai.google.dev/pricing

---

### ❌ Problem: Audyt się wywala w połowie

**Błąd:**
```
⏳ Pobieranie strony... 25%
❌ Błąd audytu: Error: Unexpected error
```

**Krok 1: Sprawdź logi backendu**
```bash
sudo journalctl -u seoaiditor -n 100 | grep -i error
```

**Najczęstsze błędy:**

**1. Worker timeout:**
```
[CRITICAL] WORKER TIMEOUT (pid:12345)
```

**Rozwiązanie:** Zwiększ timeout w service:
```bash
sudo nano /etc/systemd/system/seoaiditor.service
```

Dodaj `--timeout 120`:
```ini
ExecStart=/var/www/seo-aiditor/venv/bin/gunicorn --workers 3 --timeout 120 --bind 0.0.0.0:5000 wsgi:app
```

Restart:
```bash
sudo systemctl daemon-reload
sudo systemctl restart seoaiditor
```

---

**2. Out of memory:**
```
MemoryError: Unable to allocate array
```

**Rozwiązanie:** Zmniejsz workers:
```bash
sudo nano /etc/systemd/system/seoaiditor.service
```

Zmień `--workers 3` na `--workers 2`

Restart:
```bash
sudo systemctl daemon-reload
sudo systemctl restart seoaiditor
```

---

**3. BeautifulSoup parse error:**
```
bs4.FeatureNotFound: Couldn't find a tree builder
```

**Rozwiązanie:**
```bash
cd /var/www/seo-aiditor
source venv/bin/activate
pip install lxml html5lib
deactivate
sudo systemctl restart seoaiditor
```

---

## Problemy z API keys

### ❌ Problem: Panel API keys nie zapisuje kluczy

**Objawy:**
- Wprowadzam klucz → klikam "Save & Continue"
- Panel się zamyka ale po odświeżeniu klucz zniknął
- Audyt pokazuje błąd "Gemini API key is required"

**Przyczyna:** LocalStorage/SessionStorage zablokowany w przeglądarce.

**Rozwiązanie:**

**1. Sprawdź Console DevTools:**
- Naciśnij `F12` (otwórz DevTools)
- Kliknij zakładkę **Console**
- Odśwież stronę (`F5`)

**Szukaj błędów:**
```
Error: localStorage is not defined
DOMException: Access is denied for this document
```

**2. Włącz cookies/localStorage:**
- Chrome: Settings → Privacy → Allow all cookies
- Firefox: Settings → Privacy → Custom → ✅ Cookies
- Wyłącz tryb prywatny / incognito

**3. Test localStorage w Console:**
```javascript
localStorage.setItem('test', 'value');
localStorage.getItem('test');
```

**Powinno zwrócić:** `"value"`

**Jeśli błąd:** Przeglądarka blokuje storage → użyj innej przeglądarki lub wyłącz blokady.

---

### ❌ Problem: Panel pokazuje stary klucz mimo że go usunąłem

**Rozwiązanie - wyczyść localStorage:**

**Console DevTools:**
```javascript
localStorage.removeItem('gemini_key');
localStorage.removeItem('psi_key');
localStorage.removeItem('remember_keys');
sessionStorage.clear();
```

Odśwież stronę (`F5`).

---

### ❌ Problem: Panel nie zmienia koloru na zielony po zapisaniu kluczy

**Przyczyna:** JavaScript error lub state nie aktualizuje się.

**Krok 1: Sprawdź Console DevTools**
```
F12 → Console
```

**Szukaj czerwonych błędów.**

**Krok 2: Hard refresh**
```
Ctrl + Shift + R
```

**Krok 3: Sprawdź czy klucze są zapisane**

Console DevTools:
```javascript
localStorage.getItem('gemini_key');
sessionStorage.getItem('gemini_key');
```

**Jeśli zwraca klucz → zapisane OK, odśwież stronę.**

---

## Problemy z wydajnością

### ❌ Problem: Aplikacja działa wolno

**Krok 1: Sprawdź RAM**
```bash
free -h
```

**Jeśli `available` < 100MB:**
- Restart aplikacji: `sudo systemctl restart seoaiditor`
- Zmniejsz workers: `--workers 2` w service file

---

**Krok 2: Sprawdź CPU**
```bash
htop
```

**Jeśli Gunicorn używa > 80% CPU:**
- Zmniejsz workers
- Sprawdź logi czy nie ma zapętlonego requesta

---

**Krok 3: Sprawdź ilość requestów**
```bash
sudo journalctl -u seoaiditor --since "10 minutes ago" | grep "POST /api/audit" | wc -l
```

**Jeśli > 50 requestów w 10 minut:**
- Możliwy spam/bot
- Rozważ rate limiting (nie implementowane obecnie)

---

### ❌ Problem: Audyt trwa > 60 sekund

**Przyczyny:**
1. Wolna strona użytkownika
2. Duża strona (wiele podstron w multi-page analysis)
3. Gemini API wolno odpowiada

**Rozwiązanie:**

**1. Wyłącz multi-page analysis (tymczasowo):**
```bash
nano /var/www/seo-aiditor/config.py
```

Zmień:
```python
ENABLE_MULTI_PAGE_ANALYSIS = False
```

Restart:
```bash
sudo systemctl restart seoaiditor
```

**2. Zwiększ timeout:**
```bash
nano /var/www/seo-aiditor/config.py
```

Zmień:
```python
REQUEST_TIMEOUT = 30  # było 10
PSI_TIMEOUT = 60      # było 30
```

Restart.

---

## Błędy instalacji

### ❌ Problem: `pip3: command not found`

**Rozwiązanie:**
```bash
sudo apt update
sudo apt install -y python3-pip
```

**Weryfikacja:**
```bash
pip3 --version
```

---

### ❌ Problem: `python3-venv: Unable to locate package`

**Rozwiązanie:**
```bash
sudo apt update
sudo apt install -y python3-venv
```

**Jeśli nadal błąd:**
```bash
sudo apt install -y python3.12-venv
```

(Dostosuj `3.12` do swojej wersji Pythona)

---

### ❌ Problem: `git: command not found`

**Rozwiązanie:**
```bash
sudo apt install -y git
```

---

### ❌ Problem: `ERROR: Could not install packages` przy pip install

**Błąd:**
```
ERROR: Could not install packages due to an OSError: [Errno 28] No space left on device
```

**Rozwiązanie:** Brak miejsca na dysku
```bash
df -h
```

Jeśli Use% > 95%:
```bash
# Usuń stare logi
sudo journalctl --vacuum-time=3d

# Usuń stare backupy
find /var/www -name "*.tar.gz" -mtime +7 -delete

# Usuń apt cache
sudo apt clean
```

---

## Błędy Git

### ❌ Problem: `git pull` pokazuje conflicts

**Błąd:**
```
error: Your local changes to the following files would be overwritten by merge:
    index.html
Please commit your changes or stash them before you merge.
```

**Rozwiązanie - zachowaj zmiany lokalne:**
```bash
cd /var/www/seo-aiditor
sudo git stash
sudo git pull origin master
sudo git stash pop
```

**Rozwiązanie - porzuć zmiany lokalne:**
```bash
cd /var/www/seo-aiditor
sudo git reset --hard HEAD
sudo git pull origin master
```

---

### ❌ Problem: `git pull` pokazuje "fatal: not a git repository"

**Rozwiązanie:**
```bash
cd /var/www/seo-aiditor
sudo git init
sudo git remote add origin https://github.com/maciusman/seo-aiditor.git
sudo git fetch
sudo git reset --hard origin/master
```

---

## Problemy z SSH

### ❌ Problem: "Connection refused" przy SSH

**Przyczyny:**
1. Zły port SSH
2. Firewall blokuje
3. VPS wyłączony

**Krok 1: Sprawdź w panelu Mikr.us**
- Czy VPS jest uruchomiony?
- Jaki port SSH? (np. 12345)

**Krok 2: Użyj poprawnego portu**
```bash
ssh m1234@s1234.mikr.us -p 12345
```

(Zastąp `m1234`, `s1234`, `12345` swoimi danymi)

---

### ❌ Problem: "Permission denied (publickey)"

**Rozwiązanie:** Użyj hasła zamiast klucza
```bash
ssh -o PreferredAuthentications=password m1234@s1234.mikr.us -p 12345
```

Wpisz hasło gdy zapyta.

---

### ❌ Problem: SSH rozłącza się po kilku minutach

**Rozwiązanie:** Włącz keep-alive

Edytuj lokalny config SSH (na swoim komputerze):
```bash
nano ~/.ssh/config
```

Dodaj:
```
Host *
    ServerAliveInterval 60
    ServerAliveCountMax 3
```

Zapisz: Ctrl+O, Enter, Ctrl+X

---

## 🆘 Ostatnia deska ratunku

### Jeśli nic nie działa:

**1. Sprawdź wszystkie logi:**
```bash
# System log
sudo journalctl -xe

# Aplikacja log
sudo journalctl -u seoaiditor -n 200

# Kernel log
dmesg | tail -50
```

**2. Restart wszystkiego:**
```bash
sudo systemctl restart seoaiditor
sudo reboot
```

**3. Reinstalacja aplikacji:**
```bash
# Backup
cd /var/www
sudo tar -czf seoaiditor-emergency-backup.tar.gz seo-aiditor/

# Usuń
sudo rm -rf seo-aiditor/

# Clone ponownie
sudo git clone https://github.com/maciusman/seo-aiditor.git
cd seo-aiditor

# Venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
deactivate

# Service
sudo systemctl restart seoaiditor
```

---

## 📞 Gdzie szukać pomocy

1. **GitHub Issues:** https://github.com/maciusman/seo-aiditor/issues
2. **Mikr.us Wiki:** https://wiki.mikr.us/
3. **Mikr.us Forum:** https://www.facebook.com/groups/mikrus

**Gdy zgłaszasz problem, dołącz:**
- Dokładny błąd z logów: `sudo journalctl -u seoaiditor -n 50`
- Output systemctl status: `sudo systemctl status seoaiditor`
- Wersja systemu: `cat /etc/os-release`
- Wersja Pythona: `python3 --version`

---

**Powodzenia!** 🔧

Większość problemów rozwiązują się poprzez:
1. Sprawdzenie logów: `sudo journalctl -u seoaiditor -n 50`
2. Restart aplikacji: `sudo systemctl restart seoaiditor`
3. Sprawdzenie tej dokumentacji 📚
