#!/usr/bin/env python3
"""
SEO AIditor - Automatyczne uruchomienie (Cross-platform)
Uruchamia backend Flask + otwiera przeglądarkę
"""

import os
import sys
import time
import subprocess
import webbrowser
from pathlib import Path

def print_banner():
    """Wyświetl banner"""
    print("=" * 50)
    print("   SEO AIditor - Uruchamianie...")
    print("=" * 50)
    print()

def check_python():
    """Sprawdź wersję Pythona"""
    if sys.version_info < (3, 8):
        print("[BŁĄD] Wymagany Python 3.8 lub nowszy!")
        print(f"Twoja wersja: {sys.version}")
        return False
    return True

def check_dependencies():
    """Sprawdź czy zainstalowane są zależności"""
    print("[1/4] Sprawdzam zależności...")
    try:
        import flask
        import flask_cors
        import requests
        import bs4
        print("✓ Wszystkie zależności zainstalowane")
        return True
    except ImportError as e:
        print(f"[!] Brak zależności: {e.name}")
        print("[!] Instaluję zależności...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
            print("✓ Zależności zainstalowane")
            return True
        except subprocess.CalledProcessError:
            print("[BŁĄD] Nie udało się zainstalować zależności!")
            return False

def check_config():
    """Sprawdź czy istnieje config_local.py"""
    print("[2/4] Sprawdzam konfigurację...")

    if not Path("config_local.py").exists():
        print()
        print("[UWAGA] Brak pliku config_local.py!")
        print()
        print("Skopiuj config_local.example.py jako config_local.py")
        print("i wstaw swoje klucze API.")
        print()

        # Automatycznie skopiuj example jeśli istnieje
        if Path("config_local.example.py").exists():
            import shutil
            response = input("Czy chcesz automatycznie skopiować szablon? (t/n): ")
            if response.lower() in ['t', 'y', 'tak', 'yes']:
                shutil.copy("config_local.example.py", "config_local.py")
                print("✓ Plik config_local.py utworzony")
                print("! Teraz edytuj config_local.py i wstaw swoje klucze API")
                return False
        return False

    print("✓ Konfiguracja OK")
    return True

def start_backend():
    """Uruchom backend Flask w tle"""
    print("[3/4] Uruchamiam backend Flask...")

    try:
        # Uruchom app.py w tle
        if sys.platform == "win32":
            # Windows: użyj CREATE_NEW_CONSOLE aby uruchomić w nowym oknie
            subprocess.Popen(
                [sys.executable, "app.py"],
                creationflags=subprocess.CREATE_NEW_CONSOLE
            )
        else:
            # Linux/Mac: uruchom w tle
            subprocess.Popen(
                [sys.executable, "app.py"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

        print("✓ Backend uruchomiony")
        return True
    except Exception as e:
        print(f"[BŁĄD] Nie udało się uruchomić backendu: {e}")
        return False

def open_browser():
    """Otwórz przeglądarkę"""
    print("[4/4] Otwieram przeglądarkę...")

    # Poczekaj na uruchomienie serwera
    print("Czekam na uruchomienie serwera...")
    time.sleep(3)

    # Otwórz backend URL
    try:
        webbrowser.open("http://localhost:5000")
        print("✓ Przeglądarka otwarta")
    except Exception as e:
        print(f"[UWAGA] Nie udało się otworzyć przeglądarki: {e}")
        print("Otwórz ręcznie: http://localhost:5000")

    # Spróbuj też otworzyć index.html jako backup
    time.sleep(1)
    try:
        index_path = Path("index.html").resolve()
        webbrowser.open(f"file://{index_path}")
    except:
        pass

def main():
    """Główna funkcja"""
    print_banner()

    # Sprawdź Python
    if not check_python():
        input("\nNaciśnij Enter aby zakończyć...")
        return 1

    # Sprawdź zależności
    if not check_dependencies():
        input("\nNaciśnij Enter aby zakończyć...")
        return 1

    # Sprawdź konfigurację
    if not check_config():
        input("\nNaciśnij Enter aby zakończyć...")
        return 1

    # Uruchom backend
    if not start_backend():
        input("\nNaciśnij Enter aby zakończyć...")
        return 1

    # Otwórz przeglądarkę
    open_browser()

    # Success!
    print()
    print("=" * 50)
    print("   SEO AIditor uruchomiony!")
    print("=" * 50)
    print()
    print("Backend: http://localhost:5000")
    print("Frontend: index.html")
    print()
    print("Aby zatrzymać backend:")
    print("- Windows: Zamknij okno z backendem")
    print("- Mac/Linux: Znajdź proces i zabij (pkill -f app.py)")
    print()

    input("Naciśnij Enter aby zakończyć...")
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n[!] Przerwano przez użytkownika")
        sys.exit(0)
