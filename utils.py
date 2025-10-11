# utils.py
import requests
import validators
from urllib.parse import urlparse, urljoin
from config import REQUEST_TIMEOUT, USER_AGENT
from bs4 import BeautifulSoup
import re

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


def extract_visible_text(html_content, max_length=50000):
    """
    Extract only visible body text from HTML (remove scripts, styles, metadata).

    Critical for AI analysis - prevents analyzing metadata instead of actual content.

    Args:
        html_content: Full HTML string
        max_length: Maximum characters to return (default 50k)

    Returns:
        str: Cleaned visible text from page body
    """
    try:
        soup = BeautifulSoup(html_content, 'html.parser')

        # Remove non-visible elements
        for tag in soup(['script', 'style', 'meta', 'link', 'noscript', 'iframe', 'svg']):
            tag.decompose()

        # Extract from body only (if exists)
        body = soup.find('body')
        if body:
            visible_text = body.get_text(separator='\n', strip=True)
        else:
            visible_text = soup.get_text(separator='\n', strip=True)

        # Clean up excessive whitespace
        lines = [line.strip() for line in visible_text.split('\n') if line.strip()]
        visible_text = '\n'.join(lines)

        # Truncate to max_length
        if len(visible_text) > max_length:
            visible_text = visible_text[:max_length]

        return visible_text

    except Exception as e:
        print(f"[extract_visible_text] Error: {e}")
        # Fallback: return raw HTML excerpt
        return html_content[:max_length]


def detect_page_type(html_content):
    """
    Detect page type for context-aware AI analysis.

    Types:
    - homepage: Site homepage (root URL)
    - product: E-commerce product page
    - category: Category/listing page
    - article: Blog post/article
    - corporate: About/Company/Team page
    - contact: Contact page
    - unknown: Cannot determine

    Args:
        html_content: Full HTML string

    Returns:
        str: Page type
    """
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        html_lower = html_content.lower()

        # Check Schema.org markup (most reliable)
        schema_scripts = soup.find_all('script', type='application/ld+json')
        for script in schema_scripts:
            script_content = script.string
            if script_content:
                if '"@type":"product"' in script_content.lower():
                    return 'product'
                if '"@type":"article"' in script_content.lower() or '"@type":"blogposting"' in script_content.lower():
                    return 'article'

        # Check Open Graph type
        og_type = soup.find('meta', property='og:type')
        if og_type and og_type.get('content'):
            content = og_type['content'].lower()
            if 'product' in content:
                return 'product'
            if 'article' in content:
                return 'article'

        # Check URL patterns
        title = soup.find('title')
        title_text = title.get_text().lower() if title else ''

        # Product page indicators
        if re.search(r'(add to cart|buy now|in stock|price:|\.00\s*€|\.00\s*\$)', html_lower):
            return 'product'

        # Article/blog indicators
        if re.search(r'(posted on|published|author:|by\s+\w+\s+\w+|read time|minutes? read)', html_lower):
            return 'article'

        # Corporate pages
        if re.search(r'(about us|our team|our mission|our story|company|who we are)', html_lower):
            return 'corporate'

        # Contact page
        if re.search(r'(contact us|get in touch|email us|phone:|address:)', html_lower):
            return 'contact'

        # Category/listing page indicators
        if re.search(r'(showing \d+ results|items found|filter by|sort by)', html_lower):
            return 'category'

        # Homepage indicators (usually shorter, many CTAs)
        h1_count = len(soup.find_all('h1'))
        cta_count = len(re.findall(r'(shop now|learn more|get started|sign up|free trial)', html_lower))

        if h1_count <= 1 and cta_count >= 2:
            return 'homepage'

        return 'unknown'

    except Exception as e:
        print(f"[detect_page_type] Error: {e}")
        return 'unknown'


def detect_site_type(html_content):
    """
    Detect overall site type for context-aware criteria.

    Types:
    - ecommerce: Online store
    - blog: Content/blog site
    - corporate: Company/business site
    - saas: SaaS product site
    - portfolio: Personal/agency portfolio
    - news: News/magazine site
    - unknown: Cannot determine

    Args:
        html_content: Full HTML from homepage

    Returns:
        str: Site type
    """
    try:
        html_lower = html_content.lower()

        # E-commerce indicators
        ecommerce_score = 0
        if re.search(r'(add to cart|shopping cart|checkout|shop now|buy now|free shipping)', html_lower):
            ecommerce_score += 3
        if re.search(r'(product|products|store|shop)', html_lower):
            ecommerce_score += 2
        if ecommerce_score >= 3:
            return 'ecommerce'

        # Blog indicators
        blog_score = 0
        if re.search(r'(blog|article|post|latest posts|recent articles)', html_lower):
            blog_score += 3
        if re.search(r'(read more|continue reading|posted by|author)', html_lower):
            blog_score += 2
        if blog_score >= 3:
            return 'blog'

        # SaaS indicators
        saas_score = 0
        if re.search(r'(pricing|plans|free trial|sign up|demo|dashboard)', html_lower):
            saas_score += 2
        if re.search(r'(features|integrations|api|cloud|platform)', html_lower):
            saas_score += 2
        if saas_score >= 3:
            return 'saas'

        # News site indicators
        if re.search(r'(breaking news|latest news|headlines|categories|sections)', html_lower):
            return 'news'

        # Portfolio indicators
        if re.search(r'(portfolio|projects|my work|case studies|clients)', html_lower):
            return 'portfolio'

        # Corporate (default for business sites)
        if re.search(r'(about us|services|solutions|contact|company)', html_lower):
            return 'corporate'

        return 'unknown'

    except Exception as e:
        print(f"[detect_site_type] Error: {e}")
        return 'unknown'
