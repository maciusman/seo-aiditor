# analyzers/pagespeed.py
import requests
import time
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

def analyze_pagespeed_full(url):
    """
    Full PageSpeed analysis with desktop + mobile + all Lighthouse categories
    Returns comprehensive performance data for new Performance tab
    """
    results = {
        'mobile': None,
        'desktop': None,
        'success': False,
        'error': None
    }

    try:
        # Fetch mobile data (all categories)
        mobile_data = fetch_psi_data_full(url, 'mobile')
        results['mobile'] = parse_psi_data_full(mobile_data)

        # Rate limiting: Wait 2s between requests to respect Google's rate limits
        # (Prevents 429 Too Many Requests when doing mobile + desktop in quick succession)
        time.sleep(2)

        # Fetch desktop data (all categories)
        desktop_data = fetch_psi_data_full(url, 'desktop')
        results['desktop'] = parse_psi_data_full(desktop_data)

        results['success'] = True

    except Exception as e:
        results['error'] = str(e)
        results['success'] = False

    return results

def fetch_psi_data(url, strategy='mobile'):
    """Pobierz dane z PageSpeed Insights API (tylko performance - legacy)"""
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

    # Rate limit handling - retry once after 5s if we hit 429
    if response.status_code == 429:
        print(f"  [PageSpeed] Rate limit hit (429), waiting 5s and retrying...")
        time.sleep(5)
        response = requests.get(endpoint, params=params, timeout=PSI_TIMEOUT)

    # Lepszy error handling
    if response.status_code == 403:
        raise Exception("403 Forbidden - Sprawdź uprawnienia API key w Google Cloud Console. Kliknij na API key → Edit → API restrictions → USUŃ restrykcje lub dodaj PageSpeed Insights API do listy dozwolonych.")

    response.raise_for_status()

    return response.json()

def fetch_psi_data_full(url, strategy='mobile'):
    """Pobierz pełne dane z wszystkimi kategoriami Lighthouse"""
    endpoint = 'https://www.googleapis.com/pagespeedonline/v5/runPagespeed'

    params = {
        'url': url,
        'strategy': strategy,
        'category': ['performance', 'accessibility', 'best-practices', 'seo']
    }

    # Dodaj API key tylko jeśli jest ustawiony
    if GOOGLE_PSI_API_KEY and GOOGLE_PSI_API_KEY != "YOUR_API_KEY_HERE":
        params['key'] = GOOGLE_PSI_API_KEY

    response = requests.get(endpoint, params=params, timeout=PSI_TIMEOUT)

    # Rate limit handling - retry once after 5s if we hit 429
    if response.status_code == 429:
        print(f"  [PageSpeed] Rate limit hit (429), waiting 5s and retrying...")
        time.sleep(5)
        response = requests.get(endpoint, params=params, timeout=PSI_TIMEOUT)

    if response.status_code == 403:
        raise Exception("403 Forbidden - Sprawdź uprawnienia API key")

    response.raise_for_status()

    return response.json()

def parse_psi_data_full(data):
    """Parsuj pełne dane PSI ze wszystkimi kategoriami"""
    lighthouse = data.get('lighthouseResult', {})
    audits = lighthouse.get('audits', {})
    categories = lighthouse.get('categories', {})

    # All category scores
    performance_score = int(categories.get('performance', {}).get('score', 0) * 100)
    accessibility_score = int(categories.get('accessibility', {}).get('score', 0) * 100)
    best_practices_score = int(categories.get('best-practices', {}).get('score', 0) * 100)
    seo_score = int(categories.get('seo', {}).get('score', 0) * 100)

    # Core Web Vitals
    lcp_audit = audits.get('largest-contentful-paint', {})
    fid_audit = audits.get('max-potential-fid', {})
    cls_audit = audits.get('cumulative-layout-shift', {})

    # Opportunities (top optimizations)
    opportunities = []
    for key, opp in audits.items():
        if opp.get('details', {}).get('type') == 'opportunity':
            savings_ms = opp.get('numericValue', 0)
            if savings_ms > 0:  # Only include if there's actual savings
                opportunities.append({
                    'title': opp.get('title', ''),
                    'description': opp.get('description', ''),
                    'savings_ms': savings_ms,
                    'savings_s': round(savings_ms / 1000, 2)
                })

    # Sort by savings (descending) and take top 5
    opportunities = sorted(opportunities, key=lambda x: x['savings_ms'], reverse=True)[:5]

    # Link to full PSI report
    final_url = data.get('lighthouseResult', {}).get('finalUrl', data.get('id', ''))
    psi_report_url = f"https://pagespeed.web.dev/analysis?url={final_url}"

    return {
        'scores': {
            'performance': performance_score,
            'accessibility': accessibility_score,
            'best_practices': best_practices_score,
            'seo': seo_score,
            'average': int((performance_score + accessibility_score + best_practices_score + seo_score) / 4)
        },
        'core_web_vitals': {
            'lcp': {
                'value': lcp_audit.get('numericValue', 0),
                'value_s': round(lcp_audit.get('numericValue', 0) / 1000, 2),
                'displayValue': lcp_audit.get('displayValue', 'N/A'),
                'rating': get_lcp_rating(lcp_audit.get('numericValue', 0))
            },
            'fid': {
                'value': fid_audit.get('numericValue', 0),
                'displayValue': fid_audit.get('displayValue', 'N/A'),
                'rating': get_fid_rating(fid_audit.get('numericValue', 0))
            },
            'cls': {
                'value': cls_audit.get('numericValue', 0),
                'displayValue': cls_audit.get('displayValue', 'N/A'),
                'rating': get_cls_rating(cls_audit.get('numericValue', 0))
            }
        },
        'opportunities': opportunities,
        'psi_report_url': psi_report_url
    }

def get_lcp_rating(value_ms):
    """Get LCP rating (good/needs-improvement/poor)"""
    if value_ms <= 2500:
        return 'good'
    elif value_ms <= 4000:
        return 'needs-improvement'
    else:
        return 'poor'

def get_fid_rating(value_ms):
    """Get FID rating"""
    if value_ms <= 100:
        return 'good'
    elif value_ms <= 300:
        return 'needs-improvement'
    else:
        return 'poor'

def get_cls_rating(value):
    """Get CLS rating"""
    if value <= 0.1:
        return 'good'
    elif value <= 0.25:
        return 'needs-improvement'
    else:
        return 'poor'

def parse_psi_data(data):
    """Parsuj dane z PSI API (legacy - tylko performance)"""
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
