# analyzers/ai_intent_analysis.py
"""
Search Intent Match Analysis using Gemini 2.5 Flash

Analyzes if page content matches user search intent:
- Intent type detection (informational, navigational, transactional, commercial)
- Page structure alignment with intent
- Content depth appropriateness
- Intent mismatch identification
"""

import os
import json
from ai_engine import get_gemini_model

def analyze_search_intent_match(url, html_content, primary_keywords, language='en'):
    """
    Analyze if page content matches search intent for target keywords.

    Uses Gemini's 1M context window to analyze FULL page content deeply.

    Args:
        url: Target URL
        html_content: Full HTML content (can be up to 100k tokens!)
        primary_keywords: Target keywords
        language: Detected page language (en, pl, de, es, fr, etc.)

    Returns:
        dict: Intent analysis results
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

    # Truncate HTML to 100k characters (~75k words, well within 1M token limit)
    html_excerpt = html_content[:100000]

    keywords_str = ", ".join(primary_keywords) if isinstance(primary_keywords, list) else primary_keywords

    prompt = f"""{lang_instruction}

Analyze search intent match for: {url}

Target keywords: {keywords_str}

Full page HTML (analyze deeply):
{html_excerpt}

Tasks:

1. DETECT PRIMARY SEARCH INTENT:
   - Informational: User wants to learn/understand something
   - Navigational: User wants to find specific brand/website
   - Transactional: User ready to buy/convert/take action
   - Commercial: User researching before buying (comparison, reviews)

   Consider:
   - What would someone searching these keywords want to achieve?
   - What stage of buyer journey are they in?

2. PAGE STRUCTURE MATCH:
   - Does page structure align with detected intent?

   Examples:
   - Transactional intent needs: Clear CTAs, pricing, "Buy now" buttons, trust signals
   - Informational intent needs: Comprehensive content, explanations, examples
   - Commercial intent needs: Comparisons, pros/cons, reviews, recommendations
   - Navigational intent needs: Clear branding, contact info, navigation

3. CONTENT DEPTH MATCH:
   - Is content depth appropriate for intent?

   Examples:
   - Informational queries need detailed, comprehensive answers
   - Transactional queries need concise info + clear path to action
   - Commercial queries need balanced, comparative information

4. IDENTIFY MISMATCHES:
   - Structure mismatches (e.g., blog post format for transactional query)
   - Content mismatches (e.g., too brief for informational intent)
   - CTA mismatches (e.g., no clear CTA for transactional intent)
   - Tone mismatches (e.g., salesy tone for informational query)

5. CALCULATE INTENT SCORE:
   - How well does page match detected intent? (0-100)
   - 0-40: Severe mismatch (wrong intent entirely)
   - 41-65: Partial match (some elements present, others missing)
   - 66-85: Good match (most elements aligned)
   - 86-100: Perfect match (ideal structure + content for intent)

Return valid JSON:
{{
    "detected_intent": "informational|navigational|transactional|commercial",
    "intent_confidence": 0-100,
    "intent_reasoning": "Why this intent? (2-3 sentences)",
    "page_structure_match": true/false,
    "structure_details": "What's aligned/misaligned",
    "content_depth_match": true/false,
    "depth_details": "Is content deep enough for this intent?",
    "mismatches": [
        "Mismatch 1: Blog structure for transactional query",
        "Mismatch 2: No clear CTA despite buying intent",
        ...
    ],
    "recommendations": [
        "Add clear pricing section with CTA",
        "Restructure as product page, not blog post",
        ...
    ],
    "intent_score": 0-100,
    "verdict": "perfect_match|good_match|partial_match|mismatch"
}}

IMPORTANT:
- Analyze the FULL HTML provided (not just excerpt)
- Look at actual page elements (headings, CTAs, structure)
- Be specific about mismatches
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
        print(f"[Intent Analysis] JSON decode error: {e}")
        print(f"Raw response: {response.text[:500]}")
        return {
            'success': False,
            'error': 'JSON parsing failed',
            'intent_score': 50
        }

    except Exception as e:
        print(f"[Intent Analysis] Error: {e}")
        return {
            'success': False,
            'error': str(e),
            'intent_score': 50
        }
