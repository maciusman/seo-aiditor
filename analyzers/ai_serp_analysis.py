# analyzers/ai_serp_analysis.py
"""
SERP Position & Competitive Analysis using Gemini 2.5 Flash with Grounding

Uses Google Search grounding to:
1. Check current ranking position for target keywords
2. Analyze top 3 competitors
3. Identify content gaps vs competitors
4. Generate competitive insights
"""

import os
import json
from ai_engine import get_gemini_model

def analyze_serp_position(url, primary_keywords, language='en'):
    """
    Analyze SERP position and competitive landscape using Google Search grounding.

    Args:
        url: Target URL to analyze
        primary_keywords: List of primary keywords (auto-detected from meta title + H1)
        language: Detected page language (en, pl, de, es, fr, etc.)

    Returns:
        dict: SERP analysis with competitive insights
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

    # Format keywords for prompt
    keywords_str = ", ".join(primary_keywords) if isinstance(primary_keywords, list) else primary_keywords

    prompt = f"""{lang_instruction}

Analyze SERP position and competitive landscape for: {url}

Target keywords: {keywords_str}

Use Google Search to research these keywords and analyze:

1. RANKING POSITION:
   - Check if {url} appears in search results for these keywords
   - What position (approximately)?
   - If not ranking, explain why (possible reasons)

2. TOP 3 COMPETITORS:
   - Identify top 3 ranking URLs for these keywords
   - For each competitor:
     * URL and page title
     * Key strengths (what makes them rank well?)
     * Weaknesses (what could be improved?)
     * Content depth (comprehensive vs surface-level?)

3. CONTENT GAPS:
   - What topics/sections do competitors cover that {url} lacks?
   - What questions do competitors answer that {url} doesn't?
   - What formats do competitors use (videos, infographics, tools)?

4. OPPORTUNITIES:
   - Low-hanging fruit (easy wins to improve ranking)
   - Content upgrades (how to make content more comprehensive)
   - Unique angles (what could differentiate {url} from competitors)

5. COMPETITIVE SCORE:
   - Overall competitiveness: 0-100
   - 0-30: Far behind competitors
   - 31-60: Competitive but needs improvement
   - 61-85: Strong competitive position
   - 86-100: Market leader

Return valid JSON:
{{
    "ranking_position": number or null,
    "serp_date": "2025-10-05",
    "currently_ranking": boolean,
    "top_competitors": [
        {{
            "url": "https://competitor1.com/...",
            "title": "Page title",
            "strengths": ["strength1", "strength2", ...],
            "weaknesses": ["weakness1", ...],
            "content_depth": "comprehensive|moderate|surface"
        }}
    ],
    "content_gaps": [
        "Gap 1: Missing section about X",
        "Gap 2: No coverage of Y topic",
        ...
    ],
    "opportunities": [
        "Add comprehensive guide to X",
        "Create interactive calculator/tool",
        ...
    ],
    "competitive_score": 0-100,
    "competitive_assessment": "behind|competitive|strong|leader",
    "key_insights": "Overall competitive analysis summary (2-3 sentences)"
}}

IMPORTANT:
- Use real Google Search data via grounding
- Be specific about URLs and titles found
- Focus on actionable insights
"""

    try:
        # Generate with Google Search grounding
        response = model.generate_content(
            prompt,
            tools=[{'google_search': {}}],  # Enable Google Search grounding
            generation_config={
                'response_mime_type': 'application/json',
                'temperature': 0.3  # Lower temp for factual analysis
            }
        )

        result = json.loads(response.text)
        result['success'] = True
        result['method'] = 'gemini_grounding'

        return result

    except json.JSONDecodeError as e:
        print(f"[SERP Analysis] JSON decode error: {e}")
        print(f"Raw response: {response.text[:500]}")

        # Fallback without grounding (less accurate but better than nothing)
        return {
            'success': False,
            'error': 'JSON parsing failed',
            'competitive_score': 50,  # Neutral score
            'method': 'fallback',
            'message': 'Could not perform grounding analysis'
        }

    except Exception as e:
        print(f"[SERP Analysis] Error: {e}")
        return {
            'success': False,
            'error': str(e),
            'competitive_score': 50
        }
