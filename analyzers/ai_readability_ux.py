# analyzers/ai_readability_ux.py
"""
Readability & User Experience Analysis

Analyzes:
- Readability (Flesch-Kincaid grade level, sentence complexity)
- UX writing (CTAs, action-oriented language)
- Accessibility (alt text, link text, heading hierarchy)
- Engagement (hooks, storytelling, emotional connection)
"""

import os
import json
from ai_engine import get_gemini_model

def analyze_readability_ux(html_content, target_audience='general'):
    """
    Comprehensive readability and UX writing analysis.

    Args:
        html_content: Full HTML content
        target_audience: Target audience level ('general', 'technical', 'professional', etc.)
                        Auto-detected if not specified

    Returns:
        dict: Readability and UX analysis
    """

    model = get_gemini_model()

    html_excerpt = html_content[:100000]

    prompt = f"""
Analyze readability and UX for content.

Target audience: {target_audience} (detect actual audience from content if different)

Content:
{html_excerpt}

Evaluate:

═══════════════════════════════════
1. READABILITY
═══════════════════════════════════

Sentence complexity:
- Average sentence length? (count approximate)
- Short sentences (easy) vs long complex sentences (hard)?
- Flesch-Kincaid reading level estimate:
  * Elementary (5-7 grade)
  * Middle school (8-10 grade)
  * High school (11-12 grade)
  * College (13-16 grade)
  * Professional/Academic (17+ grade)

Paragraph structure:
- Paragraph length (short/digestible vs walls of text)?
- Use of headings (H2, H3) to break up content?
- White space and visual breathing room?

Scannability:
- Bullet points and numbered lists used?
- Bold/italics for emphasis?
- Easy to scan for key information?

═══════════════════════════════════
2. UX WRITING
═══════════════════════════════════

Clear CTAs (Call-to-Actions):
- Are CTAs present and obvious?
- Action-oriented language? ("Get started", "Try free", etc.)
- CTA placement logical?

User-centric vs company-centric:
- "You" language (user-focused) vs "We" language (company-focused)?
- Benefits-focused vs features-focused?
- Speaks to user needs/pain points?

Tone:
- Appropriate for audience?
- Conversational vs formal?
- Engaging vs dry?

═══════════════════════════════════
3. ACCESSIBILITY
═══════════════════════════════════

Alt text on images:
- Do images have alt attributes?
- Are alt texts descriptive (not just "image")?

Link text quality:
- Descriptive link text ("read our pricing guide") vs generic ("click here")?
- Links provide context about destination?

Heading hierarchy:
- Logical H1 → H2 → H3 structure?
- Headings descriptive and helpful?

Color contrast (if detectable):
- Text readable against background?
- Any potential contrast issues?

═══════════════════════════════════
4. ENGAGEMENT
═══════════════════════════════════

Hook in first paragraph:
- Does intro grab attention?
- Clear value proposition upfront?
- Compelling reason to keep reading?

Storytelling elements:
- Uses examples, anecdotes, case studies?
- Narrative flow (not just dry facts)?
- Relatable scenarios?

Emotional connection:
- Addresses user emotions/frustrations?
- Empathy shown for user problems?
- Inspires action or emotion?

═══════════════════════════════════

Return valid JSON:
{{
    "detected_audience_level": "elementary|middle|high_school|college|professional",
    "audience_match": true/false (does content match target audience?),

    "readability_grade": "elementary|middle|high_school|college|professional",
    "flesch_score_estimate": 0-100 (higher = easier to read),
    "avg_sentence_length": number,
    "sentence_complexity": "simple|moderate|complex",

    "paragraph_quality": "short_digestible|moderate|too_long",
    "uses_headings_well": true/false,
    "scannability_score": 0-100,

    "ctas_present": true/false,
    "cta_quality": "clear_actionable|present_but_weak|missing",
    "ux_writing_score": 0-100,

    "user_centric_tone": true/false (vs company-centric),
    "tone_appropriateness": 0-100,

    "alt_text_present": "all|most|some|none",
    "link_text_quality": "descriptive|mixed|generic",
    "heading_hierarchy_logical": true/false,
    "accessibility_score": 0-100,

    "has_strong_hook": true/false,
    "storytelling_present": true/false,
    "emotional_connection": "strong|moderate|weak|none",
    "engagement_score": 0-100,

    "overall_readability_score": 0-100,

    "strengths": [
        "Strength 1",
        ...
    ],

    "issues": [
        "Issue 1: Sentences too complex for general audience",
        "Issue 2: No clear CTAs present",
        ...
    ],

    "recommendations": [
        "Shorten sentences (aim for 15-20 words average)",
        "Add clear CTA in intro and conclusion",
        "Add alt text to 5 images missing it",
        ...
    ]
}}

IMPORTANT:
- Analyze full HTML provided
- Be specific about issues (cite examples if possible)
- Readability is critical for user engagement and SEO 2025
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
        print(f"[Readability Analysis] JSON decode error: {e}")
        print(f"Raw response: {response.text[:500]}")
        return {
            'success': False,
            'error': 'JSON parsing failed',
            'overall_readability_score': 50
        }

    except Exception as e:
        print(f"[Readability Analysis] Error: {e}")
        return {
            'success': False,
            'error': str(e),
            'overall_readability_score': 50
        }
