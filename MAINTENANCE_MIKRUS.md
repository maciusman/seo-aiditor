# 🛠️ Maintenance Guide - SEO AIditor na Mikr.us VPS

**Przewodnik utrzymania aplikacji w produkcji**

---

## 📋 Spis treści

1. [Codzienne sprawdzenia](#codzienne-sprawdzenia)
2. [Aktualizacja aplikacji](#aktualizacja-aplikacji)
3. [Sprawdzanie logów](#sprawdzanie-logów)
4. [Monitoring zasobów](#monitoring-zasobów)
5. [Backup i restore](#backup-i-restore)
6. [Update systemu](#update-systemu)
7. [Restart serwera](#restart-serwera)
8. [Zarządzanie API keys](#zarządzanie-api-keys)
9. [Optymalizacja wydajności](#optymalizacja-wydajności)

---

## Codzienne sprawdzenia

### ✅ Sprawdź status aplikacji

```bash
sudo systemctl status seoaiditor
```

**Szukaj:**
- `Active: active (running)` → ✅ Działa
- `Active: failed` → ⚠️ Problem, sprawdź logi

---

### ✅ Sprawdź czy strona działa

Otwórz: **https://seoaiditor.tojest.dev**

**Sprawdź:**
- ✅ Strona ładuje się szybko (< 3 sekundy)
- ✅ Panel API keys działa (żółty/zielony)
- ✅ Możesz uruchomić testowy audyt

---

### ✅ Sprawdź wykorzystanie zasobów

```bash
free -h
```

**Output przykładowy:**
```
              total        used        free      shared  buff/cache   available
Mem:          972Mi       387Mi       124Mi       8.0Mi       461Mi       467Mi
Swap:            0B          0B          0B
```

**Co sprawdzić:**
- **used** (RAM używany) powinien być **< 700MB**
- **available** (RAM dostępny) powinien być **> 200MB**

⚠️ **Jeśli RAM > 800MB używany:**
- Restart aplikacji: `sudo systemctl restart seoaiditor`
- Rozważ upgrade VPS (Mikrus 3.0 = 2GB RAM)

---

## Aktualizacja aplikacji

### 🔄 Gdy są zmiany w GitHub

**Krok 1: Przejdź do folderu aplikacji**
```bash
cd /var/www/seo-aiditor
```

**Krok 2: Pobierz zmiany z GitHub**
```bash
sudo git pull origin master
```

**Output jeśli są zmiany:**
```
Updating abc1234..def5678
Fast-forward
 index.html | 25 +++++++++++++++++--------
 app.py     | 12 +++++++-----
 2 files changed, 24 insertions(+), 13 deletions(-)
```

**Output jeśli brak zmian:**
```
Already up to date.
```

**Krok 3: Sprawdź czy requirements.txt się zmienił**
```bash
git diff HEAD@{1} requirements.txt
```

**Jeśli są zmiany (pokazuje różnice):**
```bash
source venv/bin/activate
pip install -r requirements.txt
deactivate
```

**Krok 4: Restart aplikacji**
```bash
sudo systemctl restart seoaiditor
```

**Krok 5: Weryfikacja**
```bash
sudo systemctl status seoaiditor
```

Sprawdź: `Active: active (running)`

---

### 🔄 Rollback (wróć do poprzedniej wersji)

**Jeśli nowa wersja nie działa:**

```bash
cd /var/www/seo-aiditor
sudo git log --oneline -5
```

**Output:**
```
def5678 (HEAD -> master) Fix API keys panel
abc1234 Add inline panel
xyz9012 Update deployment guide
...
```

**Wybierz poprzedni commit** (np. `abc1234`):
```bash
sudo git checkout abc1234
sudo systemctl restart seoaiditor
```

**Wróć do najnowszej wersji:**
```bash
sudo git checkout master
sudo systemctl restart seoaiditor
```

---

## Sprawdzanie logów

### 📝 Ostatnie 50 linii logów

```bash
sudo journalctl -u seoaiditor -n 50
```

**Co zobaczysz:**
```
Oct 03 18:30:15 srv42 gunicorn[12345]: [INFO] Starting gunicorn 21.2.0
Oct 03 18:30:15 srv42 gunicorn[12345]: [INFO] Listening at: http://0.0.0.0:5000
Oct 03 18:30:20 srv42 gunicorn[12346]: [INFO] GET /api/audit - 200 OK
```

---

### 📝 Live monitoring (real-time logi)

```bash
sudo journalctl -u seoaiditor -f
```

**Użycie:**
- Uruchom komendę
- Logi pojawiają się na żywo
- Otwórz aplikację w przeglądarce → zobaczysz requesty
- **Ctrl + C** żeby zakończyć

---

### 📝 Logi z ostatniej godziny

```bash
sudo journalctl -u seoaiditor --since "1 hour ago"
```

---

### 📝 Logi z konkretnej daty

```bash
sudo journalctl -u seoaiditor --since "2025-10-03 10:00" --until "2025-10-03 12:00"
```

---

### 📝 Szukaj błędów

```bash
sudo journalctl -u seoaiditor | grep -i error
```

**Najczęstsze błędy:**

**1. Import error:**
```
ModuleNotFoundError: No module named 'flask'
```
→ Reinstaluj dependencies: `pip install -r requirements.txt`

**2. Port zajęty:**
```
[ERROR] Connection in use: ('0.0.0.0', 5000)
```
→ Kill proces: `sudo lsof -ti:5000 | sudo xargs kill -9`

**3. Timeout:**
```
[CRITICAL] WORKER TIMEOUT
```
→ Zwiększ timeout w service file (dodaj `--timeout 120`)

---

## Monitoring zasobów

### 📊 htop (interaktywny monitor)

**Instalacja (jednorazowo):**
```bash
sudo apt install -y htop
```

**Uruchom:**
```bash
htop
```

**Co zobaczysz:**
```
  CPU [||||||||||||||||25.0%]     Tasks: 45, 123 thr; 1 running
  Mem [||||||||||||  387M/972M]   Load average: 0.15 0.20 0.18
  Swp [               0K/0K]      Uptime: 3 days, 12:34:56

  PID USER      PRI  NI  VIRT   RES   SHR S CPU% MEM%   TIME+  Command
12345 root       20   0  245M  78.5M 15.2M S  2.0  8.1  0:45.12 /var/www/seo-aiditor/venv/bin/python3
12346 root       20   0  243M  76.2M 14.8M S  1.0  7.8  0:42.34 /var/www/seo-aiditor/venv/bin/python3
```

**Klawisze:**
- **F10** lub **Q** → Wyjdź
- **F5** → Tree view (drzewo procesów)
- **F6** → Sortuj (wybierz MEM% lub CPU%)

**Co sprawdzić:**
- **CPU:** Gunicorn powinien być < 30% w idle
- **MEM:** Każdy worker ~70-100MB (3 workers = ~250MB total)

---

### 📊 df (użycie dysku)

```bash
df -h
```

**Output:**
```
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1        10G  4.2G  5.3G  45% /
```

**Co sprawdzić:**
- **Use%** powinien być **< 80%**
- Jeśli > 80% → usuń stare backupy, logi

---

### 📊 Użycie dysku przez aplikację

```bash
du -sh /var/www/seo-aiditor
```

**Output:**
```
156M    /var/www/seo-aiditor
```

**Breakdown (co zajmuje miejsce):**
```bash
du -sh /var/www/seo-aiditor/*
```

```
12K    /var/www/seo-aiditor/app.py
89M    /var/www/seo-aiditor/venv
45M    /var/www/seo-aiditor/.git
...
```

---

## Backup i restore

### 💾 Backup aplikacji (raz w miesiącu)

**Utwórz backup:**
```bash
cd /var/www
sudo tar -czf seoaiditor-backup-$(date +%Y%m%d).tar.gz seo-aiditor/
```

**Sprawdź backup:**
```bash
ls -lh /var/www/seoaiditor-backup-*.tar.gz
```

**Output:**
```
-rw-r--r-- 1 root root 42M Oct  3 19:00 seoaiditor-backup-20251003.tar.gz
```

---

### 💾 Backup automatyczny (cron job)

**Edytuj crontab:**
```bash
sudo crontab -e
```

**Dodaj linię (backup codziennie o 3:00 w nocy):**
```bash
0 3 * * * tar -czf /var/www/seoaiditor-backup-$(date +\%Y\%m\%d).tar.gz -C /var/www seo-aiditor/
```

**Zapisz:** Ctrl+O, Enter, Ctrl+X

**Sprawdź czy działa:**
```bash
sudo crontab -l
```

---

### 💾 Restore z backupu

**Krok 1: Zatrzymaj aplikację**
```bash
sudo systemctl stop seoaiditor
```

**Krok 2: Usuń obecny folder**
```bash
cd /var/www
sudo rm -rf seo-aiditor/
```

**Krok 3: Rozpakuj backup**
```bash
sudo tar -xzf seoaiditor-backup-20251003.tar.gz
```

**Krok 4: Uruchom aplikację**
```bash
sudo systemctl start seoaiditor
```

**Krok 5: Weryfikacja**
```bash
sudo systemctl status seoaiditor
```

---

### 💾 Czyszczenie starych backupów

**Usuń backupy starsze niż 30 dni:**
```bash
find /var/www -name "seoaiditor-backup-*.tar.gz" -mtime +30 -delete
```

**Lista backupów (sorted by date):**
```bash
ls -lht /var/www/seoaiditor-backup-*.tar.gz
```

---

## Update systemu

### 🔄 Update pakietów (raz w tygodniu)

**Krok 1: Update listy pakietów**
```bash
sudo apt update
```

**Krok 2: Upgrade pakietów**
```bash
sudo apt upgrade -y
```

**Output:**
```
Reading package lists... Done
Building dependency tree... Done
The following packages will be upgraded:
  python3 python3-pip nginx
3 upgraded, 0 newly installed, 0 to remove
```

**Krok 3: Restart aplikacji (jeśli Python zaktualizował się)**
```bash
sudo systemctl restart seoaiditor
```

---

### 🔄 Update kernela (gdy system wymaga)

**Jeśli zobaczysz:**
```
*** System restart required ***
```

**Restart serwera:**
```bash
sudo reboot
```

**Po reboot (2-3 minuty):**
- Zaloguj się ponownie przez SSH
- Sprawdź: `sudo systemctl status seoaiditor`
- Powinien być `active (running)` (auto-start!)

---

## Restart serwera

### 🔄 Restart aplikacji (bez restart VPS)

```bash
sudo systemctl restart seoaiditor
```

**Sprawdź status po 5 sekundach:**
```bash
sudo systemctl status seoaiditor
```

---

### 🔄 Pełny restart VPS

**Kiedy:**
- Po update kernela
- Jeśli system działa dziwnie
- Raz na miesiąc (clean slate)

**Komenda:**
```bash
sudo reboot
```

**Co się stanie:**
1. SSH rozłączy się
2. VPS restartuje (~2-3 minuty)
3. Aplikacja auto-startuje (systemd!)
4. Zaloguj się ponownie po 3 minutach

**Po reboot - weryfikacja:**
```bash
uptime
```

```
 19:15:32 up 2 min,  1 user,  load average: 0.15, 0.08, 0.03
```

```bash
sudo systemctl status seoaiditor
```

```
Active: active (running) since Thu 2025-10-03 19:13:45 UTC; 2min ago
```

✅ Aplikacja uruchomiła się automatycznie!

---

## Zarządzanie API keys

### 🔑 Testuj z własnymi kluczami

**W panelu aplikacji (`https://seoaiditor.tojest.dev`):**

1. Kliknij "▼ Configure" w żółtym/zielonym panelu
2. Wprowadź swoje klucze testowe
3. **NIE zaznaczaj** "Remember keys" (używaj sessionStorage)
4. Uruchom audyt testowy
5. Sprawdź logi backendu:
   ```bash
   sudo journalctl -u seoaiditor -f
   ```

**Szukaj w logach:**
```
[INFO] POST /api/audit - Request from 46.227.241.127
[INFO] Using user-provided Gemini key: AIzaSy...xxx
[INFO] Audit completed in 12.3s
```

✅ **Klucze użytkownika są używane, NIE zapisywane server-side**

---

### 🔑 Sprawdź czy klucze nie są logowane

**NIE POWINNO BYĆ w logach:**
```
❌ Gemini key: AIzaSyC...FULL_KEY_HERE
❌ PSI key: AIzaSyD...FULL_KEY_HERE
```

**Powinno być (obcięte dla bezpieczeństwa):**
```
✅ Using user-provided Gemini key: AIzaSy...xxx
✅ Using user-provided PSI key: AIzaSy...yyy
```

---

## Optymalizacja wydajności

### ⚡ Zwiększ liczbę workers (jeśli wolne)

**Sprawdź CPU cores:**
```bash
nproc
```

**Output:** `2` (Mikrus 2.1 ma ~2 vCPU)

**Rekomendowana liczba workers:**
```
workers = (2 × CPU cores) + 1
        = (2 × 2) + 1
        = 5
```

**Edytuj service:**
```bash
sudo nano /etc/systemd/system/seoaiditor.service
```

**Zmień linię:**
```ini
ExecStart=/var/www/seo-aiditor/venv/bin/gunicorn --workers 5 --bind 0.0.0.0:5000 wsgi:app
```

**Zapisz:** Ctrl+O, Enter, Ctrl+X

**Restart:**
```bash
sudo systemctl daemon-reload
sudo systemctl restart seoaiditor
```

---

### ⚡ Dodaj timeout (jeśli audyty są wolne)

**Edytuj service:**
```bash
sudo nano /etc/systemd/system/seoaiditor.service
```

**Zmień linię:**
```ini
ExecStart=/var/www/seo-aiditor/venv/bin/gunicorn --workers 3 --timeout 120 --bind 0.0.0.0:5000 wsgi:app
```

**Zapisz i restart:**
```bash
sudo systemctl daemon-reload
sudo systemctl restart seoaiditor
```

---

### ⚡ Monitoring real-time requests

**Zainstaluj tcpdump (jednorazowo):**
```bash
sudo apt install -y tcpdump
```

**Monitor incoming requests:**
```bash
sudo tcpdump -i any port 5000
```

**Co zobaczysz (live):**
```
19:30:15.123456 IP 46.227.241.127.54321 > srv42.5000: Flags [S], seq 123456
19:30:15.123789 IP srv42.5000 > 46.227.241.127.54321: Flags [S.], seq 789012, ack 123457
```

**Ctrl+C** żeby zakończyć.

---

## 📊 Checklist miesięczny

**Co miesiąc wykonaj:**

- [ ] Backup aplikacji: `tar -czf seoaiditor-backup-$(date +%Y%m%d).tar.gz -C /var/www seo-aiditor/`
- [ ] Update systemu: `sudo apt update && sudo apt upgrade -y`
- [ ] Sprawdź logi błędów: `sudo journalctl -u seoaiditor | grep -i error`
- [ ] Sprawdź wykorzystanie dysku: `df -h` (powinno być < 80%)
- [ ] Sprawdź RAM: `free -h` (powinno być available > 200MB)
- [ ] Sprawdź uptime: `uptime` (jeśli > 30 dni → rozważ restart)
- [ ] Test aplikacji: Uruchom audyt na `https://seoaiditor.tojest.dev`
- [ ] Usuń stare backupy: `find /var/www -name "seoaiditor-backup-*.tar.gz" -mtime +30 -delete`

---

## 📚 Dodatkowe komendy

### Sprawdź otwarte porty
```bash
sudo netstat -tlnp
```

### Sprawdź procesy Python
```bash
ps aux | grep python
```

### Sprawdź użycie CPU przez aplikację
```bash
top -p $(pgrep -d',' gunicorn)
```

### Sprawdź czas działania aplikacji
```bash
sudo systemctl show seoaiditor --property=ActiveEnterTimestamp
```

### Wyczyść journal logi (jeśli za duże)
```bash
sudo journalctl --vacuum-time=7d
```

---

**Powodzenia z maintenance!** 🛠️

Pytania? Sprawdź [TROUBLESHOOTING_MIKRUS.md](TROUBLESHOOTING_MIKRUS.md)
