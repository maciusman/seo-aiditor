# analyzers/technical.py
import requests
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import fetch_url, get_domain

def analyze_technical(url, page_data):
    """Analiza fundamentów technicznych"""
    results = {
        'score': 0,
        'checks': {},
        'issues': []
    }

    # 1. Status HTTP i dostępność
    if page_data['success']:
        results['checks']['http_status'] = {
            'value': page_data['status_code'],
            'pass': page_data['status_code'] == 200,
            'score': 100 if page_data['status_code'] == 200 else 0
        }

        if page_data['status_code'] != 200:
            results['issues'].append({
                'severity': 'critical',
                'title': f'Status HTTP: {page_data["status_code"]}',
                'impact': 10,
                'description': 'Strona nie jest dostępna lub zwraca błąd'
            })
    else:
        results['checks']['http_status'] = {'pass': False, 'score': 0}
        results['issues'].append({
            'severity': 'critical',
            'title': 'Strona niedostępna',
            'impact': 10,
            'description': page_data.get('error', 'Nie można pobrać strony')
        })
        return results

    # 2. SSL/HTTPS
    is_https = url.startswith('https://')
    results['checks']['ssl'] = {
        'value': is_https,
        'pass': is_https,
        'score': 100 if is_https else 0
    }

    if not is_https:
        results['issues'].append({
            'severity': 'critical',
            'title': 'Brak certyfikatu SSL',
            'impact': 10,
            'description': 'Strona nie używa HTTPS - krytyczne dla SEO i bezpieczeństwa',
            'fix': 'Zainstaluj certyfikat SSL (darmowy: Let\'s Encrypt) i przekieruj HTTP→HTTPS'
        })

    # 3. TTFB (Time to First Byte)
    ttfb = page_data['elapsed'] * 1000  # w milisekundach
    results['checks']['ttfb'] = {
        'value': f"{ttfb:.0f}ms",
        'pass': ttfb < 600,
        'score': 100 if ttfb < 600 else (50 if ttfb < 1200 else 0)
    }

    if ttfb > 1200:
        results['issues'].append({
            'severity': 'important',
            'title': f'Wolny czas odpowiedzi serwera: {ttfb:.0f}ms',
            'impact': 7,
            'description': 'TTFB powinien być <600ms. Wpływa na user experience.',
            'fix': 'Optymalizuj serwer, rozważ CDN, włącz caching'
        })

    # 4. Security Headers
    headers = page_data.get('headers', {})
    security_headers = {
        'Strict-Transport-Security': 'HSTS',
        'X-Content-Type-Options': 'X-Content-Type',
        'X-Frame-Options': 'X-Frame',
        'Content-Security-Policy': 'CSP'
    }

    missing_headers = []
    for header, name in security_headers.items():
        if header not in headers:
            missing_headers.append(name)

    results['checks']['security_headers'] = {
        'value': f"{len(security_headers) - len(missing_headers)}/{len(security_headers)}",
        'pass': len(missing_headers) == 0,
        'score': int(((len(security_headers) - len(missing_headers)) / len(security_headers)) * 100)
    }

    if missing_headers:
        results['issues'].append({
            'severity': 'recommendation',
            'title': f'Brakuje {len(missing_headers)} security headers',
            'impact': 4,
            'description': f'Brak: {", ".join(missing_headers)}',
            'fix': 'Dodaj security headers w konfiguracji serwera'
        })

    # Oblicz średni score
    scores = [check['score'] for check in results['checks'].values()]
    results['score'] = sum(scores) / len(scores) if scores else 0

    return results
