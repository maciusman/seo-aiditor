# analyzers/ai_eeat_analysis.py
"""
E-E-A-T Signals Analysis (Experience, Expertise, Authoritativeness, Trustworthiness)

Critical for Google 2025 - comprehensive analysis of E-E-A-T signals.
"""

import os
import json
from ai_engine import get_gemini_model

def analyze_eeat_signals(url, html_content, language='en'):
    """
    Comprehensive E-E-A-T analysis using Gemini's deep understanding.

    Analyzes all 4 E-E-A-T pillars:
    - Experience (E): First-hand experience demonstrated
    - Expertise (E): Subject matter expertise shown
    - Authoritativeness (A): Authority/credibility signals
    - Trustworthiness (T): Trust and transparency signals

    Args:
        url: Target URL
        html_content: Full HTML content
        language: Detected page language (en, pl, de, es, fr, etc.)

    Returns:
        dict: E-E-A-T analysis with scores for each pillar
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

    # Use up to 100k chars of HTML (deep analysis)
    html_excerpt = html_content[:100000]

    prompt = f"""{lang_instruction}

Analyze E-E-A-T signals for: {url}

Full page content:
{html_excerpt}

Evaluate all 4 E-E-A-T pillars:

═══════════════════════════════════
1. EXPERIENCE (E) - Score 0-100
═══════════════════════════════════

First-hand experience demonstrated?

Look for:
✓ Personal anecdotes, case studies, real examples
✓ "I tried...", "In my experience...", "We tested..."
✓ Before/after photos, screenshots, data from own testing
✓ Authentic voice (not generic/AI-generated content)
✓ Specific details only someone with experience would know

Red flags:
✗ Generic content that could be written by anyone
✗ No personal experience or testing mentioned
✗ Lacks specific, practical details
✗ Reads like rewritten Wikipedia content

═══════════════════════════════════
2. EXPERTISE (E) - Score 0-100
═══════════════════════════════════

Subject matter expertise shown?

Look for:
✓ Author credentials displayed (degrees, certifications, job title)
✓ Technical depth appropriate for topic
✓ Industry-specific terminology used correctly
✓ Explains complex concepts clearly
✓ Cites authoritative sources/studies
✓ Author bio with relevant background

Red flags:
✗ No author attribution
✗ Surface-level content lacking depth
✗ Technical errors or misconceptions
✗ No demonstration of subject expertise

═══════════════════════════════════
3. AUTHORITATIVENESS (A) - Score 0-100
═══════════════════════════════════

Authority/credibility of site/author?

Look for:
✓ Author bio with credentials
✓ Links to authoritative sources (research, studies, official docs)
✓ Published in reputable publications? (if detectable)
✓ Brand signals: About Us page, company history
✓ Industry recognition, awards, certifications
✓ Social proof (testimonials, case studies)

Red flags:
✗ Anonymous content (no author)
✗ No About page or company info
✗ No external credible citations
✗ Thin brand presence

═══════════════════════════════════
4. TRUSTWORTHINESS (T) - Score 0-100
═══════════════════════════════════

Trust & transparency signals?

Look for:
✓ Clear contact information (email, phone, address)
✓ Privacy policy, terms of service present
✓ Transparent about affiliations, sponsored content
✓ HTTPS security (detectable from URL)
✓ Date published/updated shown
✓ Fact-checking, sources cited
✓ Correction policy (if applicable)

Red flags:
✗ No contact info
✗ Missing privacy policy
✗ Hidden affiliations
✗ No dates (content freshness unclear)
✗ HTTP (not HTTPS)

═══════════════════════════════════

Return valid JSON:
{{
    "experience_score": 0-100,
    "experience_signals": ["signal1", "signal2", ...],
    "experience_issues": ["issue1", ...],

    "expertise_score": 0-100,
    "expertise_signals": ["signal1", ...],
    "expertise_issues": ["issue1", ...],

    "authoritativeness_score": 0-100,
    "authoritativeness_signals": ["signal1", ...],
    "authoritativeness_issues": ["issue1", ...],

    "trustworthiness_score": 0-100,
    "trustworthiness_signals": ["signal1", ...],
    "trustworthiness_issues": ["issue1", ...],

    "overall_eeat_score": 0-100,

    "strengths": [
        "Strong author credentials displayed",
        "First-hand testing documented with photos",
        ...
    ],

    "critical_issues": [
        "No author attribution",
        "Missing contact information",
        ...
    ],

    "recommendations": [
        "Add author bio with credentials",
        "Include first-hand testing results",
        "Add contact page with email/phone",
        ...
    ],

    "eeat_grade": "excellent|good|needs_improvement|poor|critical"
}}

IMPORTANT:
- Be thorough - analyze full HTML provided
- Look for subtle signals (e.g., "tested by" vs generic claims)
- E-E-A-T is critical for Google 2025 - this is a high-priority analysis
"""

    try:
        response = model.generate_content(
            prompt,
            generation_config={
                'response_mime_type': 'application/json',
                'temperature': 0.1  # Very low temp for factual assessment
            }
        )

        result = json.loads(response.text)
        result['success'] = True

        return result

    except json.JSONDecodeError as e:
        print(f"[E-E-A-T Analysis] JSON decode error: {e}")
        print(f"Raw response: {response.text[:500]}")
        return {
            'success': False,
            'error': 'JSON parsing failed',
            'overall_eeat_score': 50
        }

    except Exception as e:
        print(f"[E-E-A-T Analysis] Error: {e}")
        return {
            'success': False,
            'error': str(e),
            'overall_eeat_score': 50
        }
