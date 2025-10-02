# analyzers/content.py
from bs4 import BeautifulSoup
import textstat
import re
from collections import Counter

def analyze_content(html_content):
    """Analiza jakości contentu"""
    results = {
        'score': 0,
        'checks': {},
        'issues': []
    }

    soup = BeautifulSoup(html_content, 'lxml')

    # Usuń script i style z analizy
    for script in soup(['script', 'style', 'nav', 'footer', 'header']):
        script.decompose()

    # Wyciągnij tekst
    text = soup.get_text(separator=' ', strip=True)
    text = re.sub(r'\s+', ' ', text)  # Normalizuj białe znaki

    # 1. Word count
    words = text.split()
    word_count = len(words)

    if word_count >= 1500:
        wc_score = 100
        wc_severity = None
    elif word_count >= 600:
        wc_score = 90
        wc_severity = None
    elif word_count >= 300:
        wc_score = 60
        wc_severity = 'recommendation'
    else:
        wc_score = 20
        wc_severity = 'important'

    results['checks']['word_count'] = {
        'value': f'{word_count} słów',
        'pass': word_count >= 300,
        'score': wc_score
    }

    if wc_severity:
        results['issues'].append({
            'severity': wc_severity,
            'title': f'{"Zbyt" if word_count < 300 else "Mało"} treści: {word_count} słów',
            'impact': 8 if word_count < 300 else 5,
            'description': f'Optimal: 600-1500+ słów. Thin content = słabe SEO.',
            'fix': 'Rozbuduj content do minimum 600 słów wartościowej treści'
        })

    # 2. Text-to-HTML ratio
    html_size = len(html_content)
    text_size = len(text)
    ratio = (text_size / html_size * 100) if html_size > 0 else 0

    results['checks']['text_html_ratio'] = {
        'value': f'{ratio:.1f}%',
        'pass': ratio >= 15,
        'score': 100 if ratio >= 15 else int(ratio / 15 * 100)
    }

    if ratio < 15:
        results['issues'].append({
            'severity': 'recommendation',
            'title': f'Niski text-to-HTML ratio: {ratio:.1f}%',
            'impact': 4,
            'description': 'Za dużo kodu, za mało tekstu (optimal >15%)',
            'fix': 'Dodaj więcej content lub uprość HTML'
        })

    # 3. Readability (Flesch Reading Ease dla angielskiego, approx dla PL)
    if word_count > 50:
        try:
            # textstat domyślnie dla EN, ale daje orientacyjną wartość
            reading_ease = textstat.flesch_reading_ease(text)

            # Interpretacja (im wyższy wynik tym łatwiejszy tekst)
            if reading_ease >= 60:
                read_score = 100
                read_label = 'Łatwy'
            elif reading_ease >= 50:
                read_score = 80
                read_label = 'Średni'
            else:
                read_score = 60
                read_label = 'Trudny'

            results['checks']['readability'] = {
                'value': f'{reading_ease:.0f} ({read_label})',
                'pass': reading_ease >= 50,
                'score': read_score
            }

            if reading_ease < 50:
                results['issues'].append({
                    'severity': 'recommendation',
                    'title': 'Tekst trudny w czytaniu',
                    'impact': 3,
                    'description': f'Readability score: {reading_ease:.0f} (im wyższy tym lepiej)',
                    'fix': 'Używaj krótszych zdań i prostszego języka'
                })
        except:
            results['checks']['readability'] = {'value': 'N/A', 'pass': True, 'score': 70}
    else:
        results['checks']['readability'] = {'value': 'Za mało tekstu', 'pass': False, 'score': 0}

    # 4. Keyword density (przykład - wykryj najpopularniejsze słowa)
    # Usuń stop words (uproszczona wersja)
    stop_words = {'i', 'w', 'z', 'na', 'do', 'się', 'to', 'że', 'po', 'jest', 'być', 'o', 'ale', 'dla', 'od', 'przez', 'oraz', 'jak', 'jako', 'więcej', 'też', 'już', 'tylko', 'bardzo', 'był', 'może', 'można', 'we', 'ze', 'and', 'the', 'a', 'an', 'of', 'to', 'in', 'for', 'on', 'with', 'at', 'by', 'from', 'as', 'is', 'are', 'was', 'were'}

    clean_words = [word.lower() for word in words if len(word) > 3 and word.lower() not in stop_words]

    if clean_words:
        word_freq = Counter(clean_words)
        top_keywords = word_freq.most_common(5)
        top_word, top_count = top_keywords[0] if top_keywords else ('N/A', 0)

        keyword_density = (top_count / len(words) * 100) if words else 0

        results['checks']['keyword_density'] = {
            'value': f'{keyword_density:.1f}% ("{top_word}")',
            'pass': 1 <= keyword_density <= 3,
            'score': 100 if 1 <= keyword_density <= 3 else (50 if keyword_density < 5 else 0),
            'top_keywords': [(kw, cnt) for kw, cnt in top_keywords]
        }

        if keyword_density > 5:
            results['issues'].append({
                'severity': 'important',
                'title': f'Keyword stuffing: "{top_word}" ({keyword_density:.1f}%)',
                'impact': 7,
                'description': 'Zbyt wysoka gęstość słowa kluczowego (>5% = spam)',
                'fix': 'Użyj synonimy i bardziej naturalnego języka'
            })
    else:
        results['checks']['keyword_density'] = {'value': 'N/A', 'pass': True, 'score': 70}

    # 5. Paragraph analysis
    paragraphs = soup.find_all('p')
    long_paragraphs = [p for p in paragraphs if len(p.get_text().split()) > 150]

    results['checks']['paragraphs'] = {
        'value': f'{len(paragraphs)} paragrafów',
        'pass': len(long_paragraphs) < len(paragraphs) * 0.3,
        'score': 100 if len(long_paragraphs) == 0 else 70
    }

    if len(long_paragraphs) > 0:
        results['issues'].append({
            'severity': 'recommendation',
            'title': f'{len(long_paragraphs)} długich paragrafów (>150 słów)',
            'impact': 3,
            'description': 'Długie paragrafy utrudniają czytanie',
            'fix': 'Podziel długie paragrafy na krótsze (50-100 słów)'
        })

    # Oblicz średni score
    scores = [check['score'] for check in results['checks'].values()]
    results['score'] = sum(scores) / len(scores) if scores else 0

    return results
