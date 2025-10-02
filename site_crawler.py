# site_crawler.py
# Multi-Page Intelligent Site Crawler for SEO AIditor

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from utils import validate_url
from config import REQUEST_TIMEOUT, USER_AGENT

def crawl_homepage(url):
    """
    Fetch homepage HTML and extract internal links

    Returns:
        dict: {
            'success': bool,
            'html': str,
            'links': list,
            'error': str (if failed)
        }
    """
    try:
        headers = {'User-Agent': USER_AGENT}
        response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()

        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        # Extract internal links
        base_domain = urlparse(url).netloc
        internal_links = set()

        for link in soup.find_all('a', href=True):
            href = link['href']
            absolute_url = urljoin(url, href)

            # Only internal links, no anchors, no duplicates
            parsed = urlparse(absolute_url)
            if parsed.netloc == base_domain:
                # Remove fragment and query params for cleaner URLs
                clean_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
                if clean_url != url and clean_url.startswith('http'):
                    internal_links.add(clean_url)

        return {
            'success': True,
            'html': html,
            'links': list(internal_links)[:100],  # Limit to 100 links for AI processing
            'status_code': response.status_code
        }

    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'html': '',
            'links': []
        }


def fetch_selected_pages(urls, timeout_per_page=10):
    """
    Fetch multiple pages in parallel using ThreadPoolExecutor

    Args:
        urls: list of URLs to fetch
        timeout_per_page: timeout in seconds per page

    Returns:
        list: [{
            'url': str,
            'success': bool,
            'html': str,
            'error': str (if failed)
        }]
    """
    results = []

    def fetch_single_page(url):
        try:
            headers = {'User-Agent': USER_AGENT}
            response = requests.get(url, headers=headers, timeout=timeout_per_page)
            response.raise_for_status()

            return {
                'url': url,
                'success': True,
                'html': response.text,
                'status_code': response.status_code
            }
        except Exception as e:
            return {
                'url': url,
                'success': False,
                'error': str(e),
                'html': ''
            }

    # Parallel fetch with ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_url = {executor.submit(fetch_single_page, url): url for url in urls}

        for future in as_completed(future_to_url):
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                url = future_to_url[future]
                results.append({
                    'url': url,
                    'success': False,
                    'error': str(e),
                    'html': ''
                })

    return results


def attempt_sitemap_fetch(url):
    """
    Try to fetch sitemap.xml to help with page discovery

    Returns:
        list: URLs found in sitemap (or empty list if not available)
    """
    try:
        parsed = urlparse(url)
        sitemap_url = f"{parsed.scheme}://{parsed.netloc}/sitemap.xml"

        headers = {'User-Agent': USER_AGENT}
        response = requests.get(sitemap_url, headers=headers, timeout=5)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            urls = [loc.text for loc in soup.find_all('loc')]
            return urls[:50]  # Limit to 50 URLs

        return []

    except:
        return []


def extract_page_metadata(html):
    """
    Extract basic metadata from HTML for AI context

    Returns:
        dict: {
            'title': str,
            'meta_description': str,
            'h1': list,
            'word_count': int
        }
    """
    try:
        soup = BeautifulSoup(html, 'html.parser')

        # Title
        title = soup.find('title')
        title_text = title.get_text(strip=True) if title else ''

        # Meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        meta_desc_text = meta_desc.get('content', '') if meta_desc else ''

        # H1 tags
        h1_tags = [h1.get_text(strip=True) for h1 in soup.find_all('h1')]

        # Word count (approximate)
        text = soup.get_text()
        word_count = len(text.split())

        return {
            'title': title_text,
            'meta_description': meta_desc_text,
            'h1': h1_tags,
            'word_count': word_count
        }

    except:
        return {
            'title': '',
            'meta_description': '',
            'h1': [],
            'word_count': 0
        }


# Test
if __name__ == '__main__':
    test_url = "https://example.com"

    print(f"[TEST] Crawling {test_url}...")
    result = crawl_homepage(test_url)

    if result['success']:
        print(f"[OK] Homepage fetched successfully")
        print(f"  - HTML length: {len(result['html'])} chars")
        print(f"  - Internal links found: {len(result['links'])}")
        print(f"  - First 5 links: {result['links'][:5]}")
    else:
        print(f"[ERROR] Failed: {result['error']}")
