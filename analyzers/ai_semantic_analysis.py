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

def analyze_semantic_seo(url, html_content, primary_keyword):
    """
    Deep semantic analysis - entities, topics, LSI keywords.

    Leverages Gemini's NLP understanding for comprehensive semantic SEO.

    Args:
        url: Target URL
        html_content: Full HTML content
        primary_keyword: Primary target keyword

    Returns:
        dict: Semantic SEO analysis
    """

    model = get_gemini_model()

    html_excerpt = html_content[:100000]
    keyword_str = primary_keyword if isinstance(primary_keyword, str) else ", ".join(primary_keyword)

    prompt = f"""
Semantic SEO analysis for: {url}
Primary keyword: {keyword_str}

Content:
{html_excerpt}

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
- What related topics SHOULD be covered but aren't?
- What questions about {keyword_str} are NOT answered?
- What subtopics do comprehensive guides usually include?

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

    "topics_missing": [
        "Missing topic 1: Should cover X but doesn't",
        "Missing topic 2: No discussion of Y",
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
- Focus on what's MISSING (gaps analysis)
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
