# analyzers/onpage.py
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import THRESHOLDS
from utils import is_internal_link, get_domain

def analyze_onpage(url, html_content):
    """Analiza elementów on-page"""
    soup = BeautifulSoup(html_content, 'lxml')
    results = {
        'score': 0,
        'checks': {},
        'issues': []
    }

    # 1. Title Tag
    title_tag = soup.find('title')
    if title_tag:
        title_text = title_tag.get_text().strip()
        title_length = len(title_text)
        optimal_min, optimal_max = THRESHOLDS['title_length_optimal']

        if optimal_min <= title_length <= optimal_max:
            title_score = 100
            title_pass = True
        elif 30 <= title_length < optimal_min or optimal_max < title_length <= 70:
            title_score = 70
            title_pass = False
            results['issues'].append({
                'severity': 'important',
                'title': 'Title tag poza optymalną długością',
                'impact': 7,
                'description': f'Długość: {title_length} znaków. Optimal: {optimal_min}-{optimal_max}',
                'fix': f'{"Skróć" if title_length > optimal_max else "Wydłuż"} title do {optimal_min}-{optimal_max} znaków'
            })
        else:
            title_score = 30
            title_pass = False
            results['issues'].append({
                'severity': 'critical',
                'title': 'Title tag zbyt krótki/długi',
                'impact': 9,
                'description': f'Długość: {title_length} znaków. Drastycznie poza normą.',
                'fix': f'Przepisz title tag do długości {optimal_min}-{optimal_max} znaków'
            })

        results['checks']['title'] = {
            'value': f"{title_length} znaków",
            'text': title_text[:60] + '...' if len(title_text) > 60 else title_text,
            'pass': title_pass,
            'score': title_score
        }
    else:
        results['checks']['title'] = {'pass': False, 'score': 0}
        results['issues'].append({
            'severity': 'critical',
            'title': 'Brak title tag',
            'impact': 10,
            'description': 'Title tag jest fundamentem SEO - musi istnieć na każdej stronie',
            'fix': 'Dodaj <title>Twój Tytuł</title> w <head>'
        })

    # 2. Meta Description
    meta_desc = soup.find('meta', attrs={'name': 'description'})
    if meta_desc and meta_desc.get('content'):
        desc_text = meta_desc.get('content').strip()
        desc_length = len(desc_text)
        optimal_min, optimal_max = THRESHOLDS['meta_desc_optimal']

        desc_score = 100 if optimal_min <= desc_length <= optimal_max else 50
        results['checks']['meta_description'] = {
            'value': f"{desc_length} znaków",
            'text': desc_text[:80] + '...' if len(desc_text) > 80 else desc_text,
            'pass': optimal_min <= desc_length <= optimal_max,
            'score': desc_score
        }

        if desc_length < optimal_min or desc_length > optimal_max:
            results['issues'].append({
                'severity': 'important',
                'title': 'Meta description poza optymalną długością',
                'impact': 6,
                'description': f'Długość: {desc_length}. Optimal: {optimal_min}-{optimal_max}',
                'fix': 'Dostosuj długość meta description i dodaj CTA'
            })
    else:
        results['checks']['meta_description'] = {'pass': False, 'score': 0}
        results['issues'].append({
            'severity': 'important',
            'title': 'Brak meta description',
            'impact': 7,
            'description': 'Meta description wpływa na CTR w wynikach wyszukiwania',
            'fix': 'Dodaj <meta name="description" content="...">'
        })

    # 3. Nagłówki H1-H6
    h1_tags = soup.find_all('h1')
    h1_count = len(h1_tags)

    if h1_count == 1:
        h1_score = 100
        h1_pass = True
        h1_text = h1_tags[0].get_text().strip()
        results['checks']['h1'] = {
            'value': f"1 H1 (✓)",
            'text': h1_text[:60] + '...' if len(h1_text) > 60 else h1_text,
            'pass': True,
            'score': 100
        }
    elif h1_count == 0:
        results['checks']['h1'] = {'value': 'Brak H1', 'pass': False, 'score': 0}
        results['issues'].append({
            'severity': 'critical',
            'title': 'Brak nagłówka H1',
            'impact': 9,
            'description': 'H1 jest kluczowy dla struktury i SEO',
            'fix': 'Dodaj jeden nagłówek H1 z głównym tematem strony'
        })
    else:
        results['checks']['h1'] = {
            'value': f"{h1_count} H1 (za dużo)",
            'pass': False,
            'score': 50
        }
        results['issues'].append({
            'severity': 'important',
            'title': f'Więcej niż jeden H1 ({h1_count})',
            'impact': 6,
            'description': 'Powinna być tylko jedna H1 na stronie',
            'fix': 'Zostaw jedną H1, resztę zamień na H2'
        })

    # Hierarchia H2-H6
    heading_structure = {
        'h2': len(soup.find_all('h2')),
        'h3': len(soup.find_all('h3')),
        'h4': len(soup.find_all('h4')),
        'h5': len(soup.find_all('h5')),
        'h6': len(soup.find_all('h6'))
    }

    results['checks']['heading_structure'] = {
        'value': f"H2:{heading_structure['h2']}, H3:{heading_structure['h3']}",
        'pass': heading_structure['h2'] > 0,
        'score': 100 if heading_structure['h2'] > 0 else 70
    }

    # 4. Obrazy i Alt teksty
    images = soup.find_all('img')
    images_with_alt = [img for img in images if img.get('alt')]
    alt_percentage = (len(images_with_alt) / len(images) * 100) if images else 100

    results['checks']['images_alt'] = {
        'value': f"{len(images_with_alt)}/{len(images)} z alt",
        'pass': alt_percentage >= 90,
        'score': int(alt_percentage)
    }

    if alt_percentage < 90 and len(images) > 0:
        missing_alt = len(images) - len(images_with_alt)
        results['issues'].append({
            'severity': 'important' if alt_percentage < 50 else 'recommendation',
            'title': f'{missing_alt} obrazów bez alt',
            'impact': 8 if alt_percentage < 50 else 5,
            'description': f'{missing_alt} z {len(images)} obrazów nie ma alt tekstu',
            'fix': 'Dodaj opisowe alt teksty do wszystkich obrazów'
        })

    # 5. Open Graph tags
    og_tags = {
        'og:title': soup.find('meta', property='og:title'),
        'og:description': soup.find('meta', property='og:description'),
        'og:image': soup.find('meta', property='og:image'),
        'og:type': soup.find('meta', property='og:type')
    }

    og_present = sum(1 for tag in og_tags.values() if tag)
    results['checks']['open_graph'] = {
        'value': f"{og_present}/4 OG tags",
        'pass': og_present >= 3,
        'score': int((og_present / 4) * 100)
    }

    if og_present < 3:
        results['issues'].append({
            'severity': 'recommendation',
            'title': 'Niekompletne Open Graph tags',
            'impact': 4,
            'description': f'Brak {4 - og_present} podstawowych OG tagów dla social media',
            'fix': 'Dodaj og:title, og:description, og:image, og:type'
        })

    # 6. Linki
    all_links = soup.find_all('a', href=True)
    base_domain = get_domain(url)

    internal_links = [link for link in all_links if is_internal_link(link['href'], base_domain)]
    external_links = [link for link in all_links if not is_internal_link(link['href'], base_domain)]

    results['checks']['links'] = {
        'value': f"Wew: {len(internal_links)}, Zew: {len(external_links)}",
        'pass': 5 <= len(internal_links) <= 100,
        'score': 100 if 10 <= len(internal_links) <= 50 else 70
    }

    if len(internal_links) < 5:
        results['issues'].append({
            'severity': 'recommendation',
            'title': 'Mało linków wewnętrznych',
            'impact': 5,
            'description': f'Tylko {len(internal_links)} linków wewnętrznych',
            'fix': 'Dodaj więcej linków do innych podstron (10-30 optimal)'
        })

    # Oblicz średni score
    scores = [check['score'] for check in results['checks'].values()]
    results['score'] = sum(scores) / len(scores) if scores else 0

    return results
