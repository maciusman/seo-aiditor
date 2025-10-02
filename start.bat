@echo off
echo ========================================
echo    SEO AIditor - Uruchamianie
echo ========================================
echo.

echo [1/3] Sprawdzanie bibliotek...
pip list | findstr "Flask" >nul 2>&1
if errorlevel 1 (
    echo UWAGA: Flask nie jest zainstalowany!
    echo Instaluję biblioteki...
    pip install -r requirements.txt
    echo.
)

echo [2/3] Uruchamianie backend API...
echo Backend bedzie dostepny pod: http://localhost:5000
echo.
echo INSTRUKCJA:
echo 1. Poczekaj az zobaczysz "Running on http://127.0.0.1:5000"
echo 2. Otworz nowe okno CMD/PowerShell
echo 3. Uruchom: start index.html
echo.
echo Nacisnij Ctrl+C aby zatrzymac serwer
echo ========================================
echo.

python app.py

pause
