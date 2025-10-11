# analyzers/ai_semantic_analysis.py
"""
Semantic SEO Analysis using Gemini 2.5 Flash NLP

Deep semantic analysis beyond basic keywords:
- Entity recognition (people, places, orgs, products)
- Topic coverage & gaps
- LSI keywords (Latent Semantic Indexing)
- Semantic coherence
- Knowledge Graph alignment
"""

import os
import json
from ai_engine import get_gemini_model
from utils import extract_visible_text, detect_page_type

def analyze_semantic_seo(url, html_content, primary_keyword, language='en', page_type=None, multipage_context=None):
    """
    Deep semantic analysis - entities, topics, LSI keywords.

    Leverages Gemini's NLP understanding for comprehensive semantic SEO.

    Args:
        url: Target URL
        html_content: Full HTML content
        primary_keyword: Primary target keyword
        language: Detected page language (en, pl, de, es, fr, etc.)
        page_type: Page type (homepage/product/article/etc.) - auto-detected if None
        multipage_context: Dict with info about other pages (for multi-page audits)

    Returns:
        dict: Semantic SEO analysis
    """

    model = get_gemini_model()

    # Language-specific instructions
    lang_instructions = {
        'pl': "Odpowiedz PO POLSKU (JSON labels po angielsku, wartości po polsku).",
        'en': "Respond in ENGLISH.",
        'de': "Antworte auf DEUTSCH (JSON labels auf Englisch, Werte auf Deutsch).",
        'es': "Responde en ESPAÑOL (etiquetas JSON en inglés, valores en español).",
        'fr': "Répondez en FRANÇAIS (étiquettes JSON en anglais, valeurs en français)."
    }

    lang_instruction = lang_instructions.get(language, lang_instructions['en'])

    # Extract visible text only (not metadata)
    visible_text = extract_visible_text(html_content, max_length=50000)

    # Detect page type if not provided
    if not page_type:
        page_type = detect_page_type(html_content)

    keyword_str = primary_keyword if isinstance(primary_keyword, str) else ", ".join(primary_keyword)

    # Build multi-page context string
    multipage_info = ""
    if multipage_context and multipage_context.get('pages_analyzed', 0) > 1:
        multipage_info = f"""
MULTI-PAGE AUDIT CONTEXT:
- Total pages analyzed: {multipage_context.get('pages_analyzed', 'N/A')}
- Other pages in audit: {', '.join(multipage_context.get('other_page_types', []))}
- Site type: {multipage_context.get('site_type', 'unknown')}

IMPORTANT: For "topics_missing", consider what's covered on OTHER pages.
Only list topics missing from THE ENTIRE SITE, not just this page.
"""

    prompt = f"""{lang_instruction}

Semantic SEO analysis for: {url}
Primary keyword: {keyword_str}
Page type: {page_type}

{multipage_info}

VISIBLE CONTENT (scripts/metadata removed):
{visible_text}

Perform deep semantic analysis:

═══════════════════════════════════
1. ENTITIES DETECTED
═══════════════════════════════════

Identify named entities:
- PEOPLE: Names of individuals mentioned
- PLACES: Locations, cities, countries
- ORGANIZATIONS: Companies, institutions
- PRODUCTS: Specific products/services mentioned
- EVENTS: Conferences, releases, etc.

For each entity:
- How well is it contextualized?
- Is it just mentioned, or explained in depth?
- Does it align with primary keyword topic?

Context quality: "good" (well-explained), "fair" (mentioned with some context), "poor" (just named, no context)

═══════════════════════════════════
2. TOPIC COVERAGE
═══════════════════════════════════

Main topics covered:
- What are the 5-10 primary topics discussed?
- How deeply is each covered? (comprehensive vs surface-level)

Related topics MISSING (semantic gaps):

CONTEXT-AWARE ANALYSIS:
- Page type: {page_type}
  * homepage/category: High-level overview expected. Detailed info on subpages is NORMAL.
    → Only flag critical gaps (e.g., "No value proposition", "Missing product benefits")
    → Do NOT flag: "No detailed specs", "No pricing" (expected on product pages)

  * article/blog: Comprehensive single-page coverage expected.
    → Flag missing subtopics that article should address

  * product: Detailed specs, pricing, reviews expected.
    → Flag: "No specifications", "No customer reviews"

- What related topics SHOULD be covered on THIS page type but aren't?
- What questions about {{keyword_str}} are NOT answered on THIS page type?

═══════════════════════════════════
3. LSI KEYWORDS (Latent Semantic Indexing)
═══════════════════════════════════

LSI keywords PRESENT:
- Related keywords/phrases naturally present in content
- Synonyms and variations of primary keyword
- Co-occurring terms (words that commonly appear with main keyword)

LSI keywords MISSING:
- Important related terms that SHOULD be present
- Common variations/synonyms not used
- Industry terms missing

═══════════════════════════════════
4. SEMANTIC COHERENCE
═══════════════════════════════════

Content flow & interconnection:
- Does content flow logically from topic to topic?
- Are topics interconnected well (not just disconnected sections)?
- Keyword stuffing vs natural keyword usage?
- Does it read naturally or forced?

Coherence score: 0-100

═══════════════════════════════════
5. KNOWLEDGE GRAPH ALIGNMENT
═══════════════════════════════════

Google Knowledge Graph opportunities:
- Do entities align with Google Knowledge Graph?
- Structured data opportunities (Schema.org)?
- Is content written in a way that helps entity extraction?

═══════════════════════════════════

Return valid JSON:
{{
    "entities_found": [
        {{
            "name": "Entity name",
            "type": "person|place|organization|product|event",
            "context_quality": "good|fair|poor",
            "mentions_count": number
        }},
        ...
    ],

    "topics_covered": [
        "Topic 1",
        "Topic 2",
        ...
    ],

    "topics_missing_critical": [
        "Critical topic 1: Essential for this page type but completely absent",
        ...
    ],

    "topics_expected_on_subpages": [
        "Topic 1: Should be on product/category pages (not homepage)",
        "Topic 2: Expected on FAQ/support pages",
        ...
    ],

    "topics_missing_opportunity": [
        "Topic 1: Would strengthen content but not essential",
        "Topic 2: Nice-to-have for differentiation",
        ...
    ],

    "lsi_keywords_present": [
        "related term 1",
        "synonym 1",
        ...
    ],

    "lsi_keywords_missing": [
        "missing term 1 (commonly used in this topic)",
        "missing variation 1",
        ...
    ],

    "semantic_coherence_score": 0-100,
    "coherence_assessment": "Natural flow, well-connected topics" or issues,

    "keyword_stuffing_detected": true/false,
    "keyword_usage_quality": "natural|somewhat_forced|stuffed",

    "knowledge_graph_opportunities": [
        "Add Schema.org Person markup for author",
        "Structure FAQ section for rich snippets",
        ...
    ],

    "semantic_score": 0-100,

    "recommendations": [
        "Add coverage of [missing topic]",
        "Incorporate LSI keywords: X, Y, Z",
        "Improve topic coherence between sections A and B",
        ...
    ]
}}

IMPORTANT:
- Use full NLP analysis capabilities
- Identify subtle semantic patterns
- Be page-type aware: Don't penalize homepage for lacking product details
- If multi-page audit: Consider site-wide coverage, not just this page
- Categorize missing topics: critical vs expected-on-subpages vs opportunity
"""

    try:
        response = model.generate_content(
            prompt,
            generation_config={
                'response_mime_type': 'application/json',
                'temperature': 0.2
            }
        )

        result = json.loads(response.text)
        result['success'] = True

        return result

    except json.JSONDecodeError as e:
        print(f"[Semantic Analysis] JSON decode error: {e}")
        print(f"Raw response: {response.text[:500]}")
        return {
            'success': False,
            'error': 'JSON parsing failed',
            'semantic_score': 50
        }

    except Exception as e:
        print(f"[Semantic Analysis] Error: {e}")
        return {
            'success': False,
            'error': str(e),
            'semantic_score': 50
        }
