# audit_engine.py
import datetime
from utils import validate_url, fetch_url
from analyzers.technical import analyze_technical
from analyzers.onpage import analyze_onpage
from analyzers.indexing import analyze_indexing
from analyzers.content import analyze_content
from analyzers.pagespeed import analyze_pagespeed
from config import WEIGHTS

def run_audit(url):
    """Uruchom pełny audyt SEO"""

    # 1. Walidacja URL
    url = validate_url(url)
    if not url:
        return {'error': 'Invalid URL'}

    # 2. Pobierz stronę
    print(f"Fetching {url}...")
    page_data = fetch_url(url)

    if not page_data['success']:
        return {
            'error': 'Cannot fetch page',
            'details': page_data.get('error')
        }

    html_content = page_data['content']

    # 3. Uruchom wszystkie analizatory
    print("Running analyzers...")

    results = {
        'url': url,
        'timestamp': datetime.datetime.now().isoformat(),
        'categories': {}
    }

    # Technical
    print("  - Technical analysis...")
    results['categories']['technical'] = analyze_technical(url, page_data)

    # On-Page
    print("  - On-page analysis...")
    results['categories']['onpage'] = analyze_onpage(url, html_content)

    # Indexing
    print("  - Indexing analysis...")
    results['categories']['indexing'] = analyze_indexing(url, html_content)

    # Content
    print("  - Content analysis...")
    results['categories']['content'] = analyze_content(html_content)

    # PageSpeed (może zająć chwilę)
    print("  - PageSpeed analysis (Google API)...")
    try:
        results['categories']['pagespeed'] = analyze_pagespeed(url)
        # Merge PageSpeed score do technical
        if 'core_web_vitals' in results['categories']['pagespeed'].get('mobile', {}):
            results['categories']['technical']['core_web_vitals'] = results['categories']['pagespeed']['mobile']['core_web_vitals']
    except Exception as e:
        print(f"    Warning: PageSpeed failed: {e}")
        results['categories']['pagespeed'] = {'score': 0, 'error': str(e)}

    # 4. Oblicz finalny score
    final_score = calculate_final_score(results['categories'])
    results['final_score'] = final_score
    results['grade'] = get_grade(final_score)

    # 5. Agreguj wszystkie issues
    all_issues = []
    for category in results['categories'].values():
        all_issues.extend(category.get('issues', []))

    # Sortuj po impact (descending)
    all_issues.sort(key=lambda x: x['impact'], reverse=True)
    results['all_issues'] = all_issues

    # 6. Quick wins (high impact, łatwe)
    results['quick_wins'] = [
        issue for issue in all_issues
        if issue['impact'] >= 6 and issue['severity'] in ['important', 'recommendation']
    ][:5]

    print("Audit complete!")
    return results

def calculate_final_score(categories):
    """Oblicz finalny wynik z wagami"""
    score = 0
    score += categories['technical']['score'] * WEIGHTS['technical']
    score += categories['onpage']['score'] * WEIGHTS['onpage']
    score += categories['indexing']['score'] * WEIGHTS['indexing']
    score += categories['content']['score'] * WEIGHTS['content']

    # PageSpeed jako część technical (już wliczone w technical)

    return round(score, 1)

def get_grade(score):
    """Określ ocenę literową"""
    if score >= 90:
        return {'label': 'EXCELLENT', 'color': 'green', 'emoji': '🟢'}
    elif score >= 75:
        return {'label': 'GOOD', 'color': 'lightgreen', 'emoji': '🟡'}
    elif score >= 60:
        return {'label': 'NEEDS IMPROVEMENT', 'color': 'yellow', 'emoji': '🟠'}
    elif score >= 40:
        return {'label': 'POOR', 'color': 'orange', 'emoji': '🔴'}
    else:
        return {'label': 'CRITICAL', 'color': 'red', 'emoji': '⛔'}

# Test
if __name__ == '__main__':
    test_url = "https://example.com"
    result = run_audit(test_url)

    print("\n=== AUDIT RESULTS ===")
    print(f"URL: {result['url']}")
    print(f"Final Score: {result['final_score']}/100 ({result['grade']['label']})")
    print(f"\nCategory Scores:")
    for cat_name, cat_data in result['categories'].items():
        print(f"  {cat_name}: {cat_data['score']:.1f}/100")

    print(f"\nTop Issues:")
    for issue in result['all_issues'][:5]:
        print(f"  [{issue['severity']}] {issue['title']} (Impact: {issue['impact']}/10)")
