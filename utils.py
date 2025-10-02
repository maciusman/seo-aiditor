# utils.py
import requests
import validators
from urllib.parse import urlparse, urljoin
from config import REQUEST_TIMEOUT, USER_AGENT

def validate_url(url):
    """Walidacja i normalizacja URL"""
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url

    if validators.url(url):
        return url
    return None

def get_domain(url):
    """Wyciągnij domenę z URL"""
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}"

def fetch_url(url, timeout=REQUEST_TIMEOUT):
    """Pobierz URL z error handling"""
    try:
        headers = {'User-Agent': USER_AGENT}
        response = requests.get(url, timeout=timeout, headers=headers, allow_redirects=True)
        return {
            'success': True,
            'status_code': response.status_code,
            'content': response.text,
            'headers': dict(response.headers),
            'url': response.url,  # final URL po redirectach
            'elapsed': response.elapsed.total_seconds()
        }
    except requests.exceptions.Timeout:
        return {'success': False, 'error': 'Timeout'}
    except requests.exceptions.RequestException as e:
        return {'success': False, 'error': str(e)}

def is_internal_link(link_url, base_domain):
    """Sprawdź czy link jest wewnętrzny"""
    if not link_url:
        return False
    link_domain = urlparse(link_url).netloc
    base = urlparse(base_domain).netloc
    return link_domain == base or link_domain == ''

def calculate_score(value, min_val, max_val, reverse=False):
    """Oblicz score 0-100 na podstawie wartości"""
    if reverse:
        value = max_val - value + min_val

    if value <= min_val:
        return 0
    elif value >= max_val:
        return 100
    else:
        return int(((value - min_val) / (max_val - min_val)) * 100)
