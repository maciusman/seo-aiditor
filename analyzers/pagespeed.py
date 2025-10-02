# analyzers/pagespeed.py
import requests
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import GOOGLE_PSI_API_KEY, PSI_TIMEOUT

def analyze_pagespeed(url):
    """Analiza Core Web Vitals via Google PageSpeed Insights API"""
    results = {
        'score': 0,
        'checks': {},
        'issues': [],
        'mobile': {},
        'desktop': {}
    }

    # Sprawdź mobilną wersję
    try:
        mobile_data = fetch_psi_data(url, 'mobile')
        results['mobile'] = parse_psi_data(mobile_data)
        results['checks']['mobile_performance'] = {
            'value': f"{results['mobile']['performance_score']}/100",
            'pass': results['mobile']['performance_score'] >= 50,
            'score': results['mobile']['performance_score']
        }

        # Core Web Vitals issues
        cwv = results['mobile']['core_web_vitals']

        # LCP
        if cwv['lcp']['value'] > 2500:
            results['issues'].append({
                'severity': 'critical' if cwv['lcp']['value'] > 4000 else 'important',
                'title': f"Wolne LCP: {cwv['lcp']['value']/1000:.1f}s (mobile)",
                'impact': 9 if cwv['lcp']['value'] > 4000 else 7,
                'description': 'Largest Contentful Paint powinien być <2.5s',
                'fix': 'Optymalizuj obrazy, użyj CDN, zminifikuj CSS/JS'
            })

        # CLS
        if cwv['cls']['value'] > 0.1:
            results['issues'].append({
                'severity': 'important' if cwv['cls']['value'] > 0.25 else 'recommendation',
                'title': f"Problemy z CLS: {cwv['cls']['value']:.3f} (mobile)",
                'impact': 7 if cwv['cls']['value'] > 0.25 else 5,
                'description': 'Cumulative Layout Shift powinien być <0.1',
                'fix': 'Dodaj wymiary do obrazów, zarezerwuj miejsce dla ads'
            })

        # FID/INP
        if cwv['fid']['value'] > 100:
            results['issues'].append({
                'severity': 'important',
                'title': f"Wolna interaktywność: {cwv['fid']['value']}ms (mobile)",
                'impact': 6,
                'description': 'First Input Delay powinien być <100ms',
                'fix': 'Zmniejsz JavaScript, użyj code splitting, defer scripts'
            })

    except Exception as e:
        results['checks']['mobile_performance'] = {
            'value': 'Error',
            'pass': False,
            'score': 0,
            'error': str(e)
        }
        results['issues'].append({
            'severity': 'important',
            'title': 'Nie udało się pobrać danych PageSpeed',
            'impact': 5,
            'description': f'Error: {str(e)[:100]}',
            'fix': 'Sprawdź API key lub spróbuj ponownie'
        })

    # Oblicz score
    if results['mobile']:
        results['score'] = results['mobile']['performance_score']
    else:
        results['score'] = 0

    return results

def fetch_psi_data(url, strategy='mobile'):
    """Pobierz dane z PageSpeed Insights API"""
    endpoint = 'https://www.googleapis.com/pagespeedonline/v5/runPagespeed'

    params = {
        'url': url,
        'strategy': strategy,  # mobile lub desktop
        'category': 'performance'
    }

    # Dodaj API key tylko jeśli jest ustawiony
    if GOOGLE_PSI_API_KEY and GOOGLE_PSI_API_KEY != "YOUR_API_KEY_HERE":
        params['key'] = GOOGLE_PSI_API_KEY

    response = requests.get(endpoint, params=params, timeout=PSI_TIMEOUT)

    # Lepszy error handling
    if response.status_code == 403:
        raise Exception("403 Forbidden - Sprawdź uprawnienia API key w Google Cloud Console. Kliknij na API key → Edit → API restrictions → USUŃ restrykcje lub dodaj PageSpeed Insights API do listy dozwolonych.")

    response.raise_for_status()

    return response.json()

def parse_psi_data(data):
    """Parsuj dane z PSI API"""
    lighthouse = data.get('lighthouseResult', {})
    audits = lighthouse.get('audits', {})

    # Performance score
    perf_score = int(lighthouse.get('categories', {}).get('performance', {}).get('score', 0) * 100)

    # Core Web Vitals
    lcp_audit = audits.get('largest-contentful-paint', {})
    fid_audit = audits.get('max-potential-fid', {})
    cls_audit = audits.get('cumulative-layout-shift', {})

    return {
        'performance_score': perf_score,
        'core_web_vitals': {
            'lcp': {
                'value': lcp_audit.get('numericValue', 0),
                'displayValue': lcp_audit.get('displayValue', 'N/A')
            },
            'fid': {
                'value': fid_audit.get('numericValue', 0),
                'displayValue': fid_audit.get('displayValue', 'N/A')
            },
            'cls': {
                'value': cls_audit.get('numericValue', 0),
                'displayValue': cls_audit.get('displayValue', 'N/A')
            }
        },
        'opportunities': [
            {
                'title': opp.get('title', ''),
                'description': opp.get('description', ''),
                'savings': opp.get('numericValue', 0)
            }
            for key, opp in audits.items()
            if opp.get('details', {}).get('type') == 'opportunity'
        ][:5]  # Top 5 opportunities
    }
