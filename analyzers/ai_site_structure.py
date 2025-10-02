# analyzers/ai_site_structure.py
# STAGE 1: AI-Powered Site Type Detection & Intelligent Page Selection

from ai_engine import AIEngine
import json

def detect_site_type_and_select_pages(url, html_content, available_links, language='en'):
    """
    STAGE 1: AI analyzes homepage and available links to:
    1. Detect site type (e-commerce, service, blog, corporate, portfolio)
    2. Intelligently select 4 additional representative pages

    Args:
        url: Homepage URL
        html_content: Homepage HTML
        available_links: List of internal links found on homepage
        language: Detected language

    Returns:
        dict: {
            'success': bool,
            'site_type': str,
            'site_characteristics': dict,
            'selected_pages': [
                {
                    'url': str,
                    'page_type': str,
                    'selection_reason': str,
                    'expected_insights': str
                }
            ],
            'error': str (if failed)
        }
    """

    # Language-specific instructions
    lang_instructions = {
        'pl': "Odpowiedz PO POLSKU (JSON labels po angielsku, wartości po polsku).",
        'en': "Respond in ENGLISH.",
        'de': "Antworte auf DEUTSCH (JSON labels auf Englisch, Werte auf Deutsch).",
        'es': "Responde en ESPAÑOL (etiquetas JSON en inglés, valores en español).",
        'fr': "Répondez en FRANÇAIS (étiquettes JSON en anglais, valeurs en français)."
    }

    lang_instruction = lang_instructions.get(language, lang_instructions['en'])

    # Format available links for AI
    links_sample = available_links[:50] if len(available_links) > 50 else available_links
    links_formatted = '\n'.join([f"- {link}" for link in links_sample])

    prompt = f"""{lang_instruction}

**YOUR ROLE:** You are a senior SEO strategist analyzing a website's structure.

**CRITICAL TASK:** Based on the homepage and available internal links, you must:
1. Detect the website type
2. Select 4 ADDITIONAL pages (not homepage) that best represent different aspects of this site

**AVAILABLE INTERNAL LINKS:**
{links_formatted}

**CRITICAL: Your entire response must be ONLY valid JSON (no markdown, no code blocks, no explanation).**

Start with opening brace and end with closing brace.

**REQUIRED JSON STRUCTURE:**

{{
  "site_type": "e-commerce|service|blog|corporate|portfolio|news|education|other",
  "site_type_confidence": 0-100,
  "site_characteristics": {{
    "primary_purpose": "string (business goal)",
    "target_audience": "string",
    "monetization_model": "string",
    "content_focus": "string"
  }},
  "selected_pages": [
    {{
      "url": "full URL from available links",
      "page_type": "category|product|service|about|blog_post|landing|contact|other",
      "selection_reason": "why this page is important for holistic analysis",
      "expected_insights": "what SEO/business insights this page will reveal"
    }}
  ]
}}

**SELECTION STRATEGY GUIDELINES:**

For E-COMMERCE sites, select:
1. Category page (shows template structure)
2. Product page (conversion optimization)
3. Blog post (content strategy)
4. About/Trust page (E-E-A-T signals)

For SERVICE sites, select:
1. Main service page (value proposition)
2. Secondary service page (breadth analysis)
3. About/Team page (authority signals)
4. Blog/Resources page (content marketing)

For BLOG/NEWS sites, select:
1. Recent article (content quality)
2. Popular/Featured article (best practices)
3. Category/Archive page (structure)
4. About/Author page (E-E-A-T)

For CORPORATE sites, select:
1. Products/Solutions page
2. About/Company page
3. Case studies/Success stories
4. Contact/CTA page

**SELECTION CRITERIA:**
- Choose pages that represent DIFFERENT templates (not 4 product pages!)
- Prioritize pages that reveal business strategy
- Select pages that show conversion funnels
- Include at least one content page (blog/article) if available
- Choose pages likely to have different SEO challenges

**CRITICAL:** You MUST select exactly 4 pages from the available links provided above.
If there are fewer than 4 distinct pages available, select the best ones available and explain in selection_reason.

**Remember:** This is STAGE 1. These pages will be fetched and analyzed holistically in STAGE 2.
Your selection directly impacts the quality of the final audit.
"""

    try:
        ai = AIEngine()

        # Use URL Context to analyze homepage
        response = ai.analyze_url(
            url=url,
            prompt=prompt,
            use_url_context=True
        )

        # Parse JSON response
        result = json.loads(response)

        # Validate required fields
        if 'site_type' not in result or 'selected_pages' not in result:
            return {
                'success': False,
                'error': 'AI response missing required fields'
            }

        # Ensure we have pages
        if not result['selected_pages'] or len(result['selected_pages']) == 0:
            return {
                'success': False,
                'error': 'AI did not select any pages'
            }

        return {
            'success': True,
            'site_type': result['site_type'],
            'site_type_confidence': result.get('site_type_confidence', 0),
            'site_characteristics': result.get('site_characteristics', {}),
            'selected_pages': result['selected_pages']
        }

    except json.JSONDecodeError as e:
        return {
            'success': False,
            'error': f'Failed to parse AI response as JSON: {str(e)}',
            'raw_response': response if 'response' in locals() else ''
        }
    except Exception as e:
        return {
            'success': False,
            'error': f'AI analysis failed: {str(e)}'
        }


# Test
if __name__ == '__main__':
    print("[TEST] AI Site Structure Analyzer")

    # Mock data
    test_url = "https://example.com"
    test_html = "<html><head><title>Example Store</title></head><body><h1>Welcome to our store</h1></body></html>"
    test_links = [
        "https://example.com/products",
        "https://example.com/products/laptop",
        "https://example.com/about",
        "https://example.com/blog/post-1",
        "https://example.com/contact"
    ]

    result = detect_site_type_and_select_pages(test_url, test_html, test_links, language='en')

    if result['success']:
        print(f"[OK] Site type detected: {result['site_type']} (confidence: {result.get('site_type_confidence', 0)}%)")
        print(f"[OK] Selected {len(result['selected_pages'])} pages:")
        for page in result['selected_pages']:
            print(f"  - {page['url']} ({page['page_type']})")
            print(f"    Reason: {page['selection_reason']}")
    else:
        print(f"[ERROR] {result['error']}")
