@echo off
REM SEO AIditor - Automatyczne uruchomienie (Windows)
REM Uruchamia backend Flask + otwiera przeglądarkę

echo ========================================
echo   SEO AIditor - Uruchamianie...
echo ========================================
echo.

REM Sprawdź czy Python jest zainstalowany
python --version >nul 2>&1
if errorlevel 1 (
    echo [BLAD] Python nie jest zainstalowany!
    echo Pobierz z: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Sprawdź czy są zainstalowane zależności
echo [1/3] Sprawdzam zaleznosci...
python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo [!] Instaluje zaleznosci...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [BLAD] Nie udalo sie zainstalowac zaleznosci!
        pause
        exit /b 1
    )
)

REM Sprawdź czy config_local.py istnieje
if not exist config_local.py (
    echo.
    echo [UWAGA] Brak pliku config_local.py!
    echo.
    echo Skopiuj config_local.example.py jako config_local.py
    echo i wstaw swoje klucze API.
    echo.
    pause
    exit /b 1
)

REM Uruchom backend w tle
echo [2/3] Uruchamiam backend Flask...
start /B python app.py

REM Poczekaj 3 sekundy na uruchomienie serwera
timeout /t 3 /nobreak >nul

REM Otwórz przeglądarkę
echo [3/3] Otwieram przegladarke...
start "" "http://localhost:5000"

REM Otwórz też frontend (index.html) jako backup
timeout /t 1 /nobreak >nul
start "" "%CD%\index.html"

echo.
echo ========================================
echo   SEO AIditor uruchomiony!
echo ========================================
echo.
echo Backend: http://localhost:5000
echo Frontend: index.html
echo.
echo Aby zatrzymac: Zamknij to okno lub nacisnij Ctrl+C
echo.
pause
