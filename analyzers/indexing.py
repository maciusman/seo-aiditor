# analyzers/indexing.py
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import xml.etree.ElementTree as ET

def analyze_indexing(url, html_content):
    """Analiza crawlability i indexing"""
    results = {
        'score': 0,
        'checks': {},
        'issues': []
    }

    soup = BeautifulSoup(html_content, 'lxml')
    base_domain = url.rstrip('/')

    # 1. Robots.txt
    robots_url = urljoin(base_domain, '/robots.txt')
    try:
        robots_response = requests.get(robots_url, timeout=5)
        if robots_response.status_code == 200:
            robots_content = robots_response.text

            # Sprawdź czy nie blokuje wszystkiego
            blocks_all = 'Disallow: /' in robots_content and 'User-agent: *' in robots_content
            has_sitemap = 'Sitemap:' in robots_content

            results['checks']['robots_txt'] = {
                'value': 'Istnieje ✓',
                'pass': not blocks_all,
                'score': 100 if (not blocks_all and has_sitemap) else 70,
                'content_preview': robots_content[:200]
            }

            if blocks_all:
                results['issues'].append({
                    'severity': 'critical',
                    'title': 'Robots.txt blokuje całą stronę',
                    'impact': 10,
                    'description': 'User-agent: * + Disallow: / blokuje indeksowanie',
                    'fix': 'NATYCHMIAST usuń lub popraw robots.txt!'
                })

            if not has_sitemap:
                results['issues'].append({
                    'severity': 'recommendation',
                    'title': 'Robots.txt nie wskazuje sitemap',
                    'impact': 3,
                    'description': 'Brak linku do sitemap.xml w robots.txt',
                    'fix': 'Dodaj linię: Sitemap: https://domain.com/sitemap.xml'
                })
        else:
            results['checks']['robots_txt'] = {
                'value': 'Brak (404)',
                'pass': True,  # Brak robots.txt nie jest błędem
                'score': 80
            }
            results['issues'].append({
                'severity': 'recommendation',
                'title': 'Brak robots.txt',
                'impact': 2,
                'description': 'Warto utworzyć robots.txt dla kontroli crawlingu',
                'fix': 'Utwórz podstawowy robots.txt ze wskazaniem sitemap'
            })
    except:
        results['checks']['robots_txt'] = {'value': 'Error', 'pass': False, 'score': 50}

    # 2. Sitemap.xml
    sitemap_url = urljoin(base_domain, '/sitemap.xml')
    try:
        sitemap_response = requests.get(sitemap_url, timeout=5)
        if sitemap_response.status_code == 200:
            # Spróbuj sparsować XML
            try:
                root = ET.fromstring(sitemap_response.content)
                # Policz URLe
                url_count = len(root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}url'))

                results['checks']['sitemap'] = {
                    'value': f'Istnieje ({url_count} URLs)',
                    'pass': True,
                    'score': 100
                }

                if url_count > 50000:
                    results['issues'].append({
                        'severity': 'important',
                        'title': 'Sitemap zbyt duża',
                        'impact': 6,
                        'description': f'{url_count} URLs (max 50,000)',
                        'fix': 'Podziel sitemap na mniejsze pliki (sitemap index)'
                    })
            except:
                results['checks']['sitemap'] = {
                    'value': 'Istnieje (niepoprawny XML)',
                    'pass': False,
                    'score': 50
                }
                results['issues'].append({
                    'severity': 'important',
                    'title': 'Sitemap niepoprawny',
                    'impact': 7,
                    'description': 'Sitemap istnieje ale ma błędy składni XML',
                    'fix': 'Napraw składnię XML w sitemap.xml'
                })
        else:
            results['checks']['sitemap'] = {
                'value': 'Brak (404)',
                'pass': False,
                'score': 0
            }
            results['issues'].append({
                'severity': 'critical',
                'title': 'Brak sitemap.xml',
                'impact': 8,
                'description': 'Sitemap pomaga Google crawlować stronę',
                'fix': 'Wygeneruj i opublikuj sitemap.xml'
            })
    except:
        results['checks']['sitemap'] = {'value': 'Error', 'pass': False, 'score': 0}

    # 3. Canonical tag
    canonical = soup.find('link', rel='canonical')
    if canonical and canonical.get('href'):
        canonical_url = canonical.get('href')
        results['checks']['canonical'] = {
            'value': 'Istnieje ✓',
            'pass': True,
            'score': 100,
            'url': canonical_url
        }
    else:
        results['checks']['canonical'] = {
            'value': 'Brak',
            'pass': False,
            'score': 60
        }
        results['issues'].append({
            'severity': 'recommendation',
            'title': 'Brak canonical tag',
            'impact': 5,
            'description': 'Canonical zapobiega duplicate content',
            'fix': 'Dodaj <link rel="canonical" href="URL"> w <head>'
        })

    # 4. Meta robots
    meta_robots = soup.find('meta', attrs={'name': 'robots'})
    if meta_robots:
        content = meta_robots.get('content', '').lower()
        is_noindex = 'noindex' in content

        results['checks']['meta_robots'] = {
            'value': content,
            'pass': not is_noindex,
            'score': 0 if is_noindex else 100
        }

        if is_noindex:
            results['issues'].append({
                'severity': 'critical',
                'title': 'Strona ma meta noindex!',
                'impact': 10,
                'description': 'Meta robots="noindex" blokuje indeksowanie',
                'fix': 'NATYCHMIAST usuń noindex lub zmień na index'
            })
    else:
        results['checks']['meta_robots'] = {
            'value': 'Brak (index by default)',
            'pass': True,
            'score': 100
        }

    # 5. Schema Markup (JSON-LD)
    schema_scripts = soup.find_all('script', type='application/ld+json')
    schema_count = len(schema_scripts)

    results['checks']['schema_markup'] = {
        'value': f'{schema_count} schema' if schema_count > 0 else 'Brak',
        'pass': schema_count > 0,
        'score': 100 if schema_count > 0 else 40
    }

    if schema_count == 0:
        results['issues'].append({
            'severity': 'recommendation',
            'title': 'Brak Schema Markup',
            'impact': 6,
            'description': 'Schema.org daje rich snippets w Google',
            'fix': 'Dodaj JSON-LD schema (Organization, Article, etc.)'
        })

    # Oblicz średni score
    scores = [check['score'] for check in results['checks'].values()]
    results['score'] = sum(scores) / len(scores) if scores else 0

    return results
