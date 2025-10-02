# analyzers/ai_multi_page.py
# STAGE 2: Holistic Multi-Page AI Analysis

from ai_engine import AIEngine
import json

def analyze_site_holistically(homepage_url, pages_data, site_type, language='en'):
    """
    STAGE 2: AI analyzes ALL pages together as ONE COHESIVE WEBSITE

    This is NOT separate per-page analysis.
    This is HOLISTIC analysis looking for:
    - Template-level issues (fix 1 template = fix N pages)
    - Content patterns across pages
    - Site-wide strategy insights
    - Conversion funnel optimization
    - Scalable recommendations

    Args:
        homepage_url: Main site URL
        pages_data: [
            {
                'url': str,
                'html': str,
                'page_type': str,
                'selection_reason': str
            }
        ]
        site_type: Detected site type from Stage 1
        language: Detected language

    Returns:
        dict: {
            'success': bool,
            'holistic_score': 0-100,
            'template_insights': [...],
            'content_patterns': {...},
            'site_strategy': {...},
            'conversion_funnel': {...},
            'scalable_recommendations': [...],
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

    # Build pages context for AI
    pages_context = []
    for i, page in enumerate(pages_data, 1):
        pages_context.append(f"""
PAGE {i}: {page['url']}
Type: {page.get('page_type', 'unknown')}
Selection Reason: {page.get('selection_reason', 'N/A')}
---
""")

    pages_formatted = '\n'.join(pages_context)

    prompt = f"""{lang_instruction}

**YOUR ROLE:** You are a senior SEO & conversion strategist performing a HOLISTIC multi-page website audit.

**CRITICAL MINDSET:**
You are analyzing ONE WEBSITE, not individual pages.
Look for PATTERNS, TEMPLATES, and SYSTEMIC issues.
Think: "If I fix this template, how many pages improve?"

**WEBSITE TYPE:** {site_type}

**PAGES TO ANALYZE TOGETHER:**
{pages_formatted}

**CRITICAL: Your entire response must be ONLY valid JSON (no markdown, no code blocks, no explanation).**

Start with opening brace and end with closing brace.

**REQUIRED JSON STRUCTURE:**

{{
  "holistic_score": 0-100,
  "executive_summary": "2-3 sentences about overall site health and biggest opportunities",

  "template_insights": [
    {{
      "template_name": "e.g., product_page, category_page, blog_post",
      "pages_affected": "approximate number or 'all product pages'",
      "critical_issues": ["issue 1", "issue 2"],
      "seo_impact": "HIGH|MEDIUM|LOW",
      "business_impact": "specific impact on conversions/revenue/leads",
      "fix_difficulty": "EASY|MEDIUM|HARD",
      "recommended_fix": "specific actionable fix",
      "expected_improvement": "quantified outcome if fixed"
    }}
  ],

  "content_patterns": {{
    "strengths": ["what's working well across pages"],
    "weaknesses": ["systematic content problems"],
    "consistency_score": 0-100,
    "brand_voice_clarity": 0-100,
    "eeat_signals": {{
      "experience": 0-100,
      "expertise": 0-100,
      "authoritativeness": 0-100,
      "trustworthiness": 0-100,
      "evidence": ["specific examples from pages"]
    }}
  }},

  "site_strategy": {{
    "primary_business_goal": "inferred from content analysis",
    "target_audience_clarity": 0-100,
    "value_proposition_strength": 0-100,
    "competitive_positioning": "string analysis",
    "content_strategy_assessment": "string analysis",
    "missing_critical_pages": ["pages that should exist but don't"]
  }},

  "conversion_funnel": {{
    "funnel_stages_present": ["awareness", "consideration", "decision", "action"],
    "funnel_gaps": ["missing stages or weak points"],
    "cta_consistency": 0-100,
    "cta_effectiveness": "analysis of calls-to-action across pages",
    "friction_points": ["obstacles preventing conversion"],
    "quick_conversion_wins": [
      {{
        "improvement": "specific change",
        "pages_affected": "which pages",
        "expected_lift": "estimated % improvement",
        "implementation_time": "hours or days"
      }}
    ]
  }},

  "scalable_recommendations": [
    {{
      "category": "TEMPLATE|CONTENT|TECHNICAL|UX",
      "priority": "CRITICAL|HIGH|MEDIUM|LOW",
      "recommendation": "specific action",
      "scope": "affects N pages or entire site",
      "business_impact": "revenue/leads/traffic impact",
      "implementation_steps": ["step 1", "step 2"],
      "time_estimate": "hours/days",
      "owner": "developer|marketer|copywriter|designer",
      "success_metric": "how to measure success"
    }}
  ],

  "cross_page_issues": [
    {{
      "issue": "problem found across multiple pages",
      "severity": "CRITICAL|HIGH|MEDIUM|LOW",
      "pages_affected": ["list of URLs or 'all pages'"],
      "root_cause": "why this is happening",
      "recommended_solution": "systemic fix"
    }}
  ],

  "roadmap": {{
    "week_1": ["immediate actions with highest ROI"],
    "month_1": ["foundational improvements"],
    "month_3": ["strategic content & SEO initiatives"],
    "ongoing": ["continuous optimization practices"]
  }}
}}

**ANALYSIS GUIDELINES:**

**THINK HOLISTICALLY:**
- Don't analyze pages in isolation
- Look for template patterns (e.g., all product pages lack schema markup)
- Identify systemic issues (e.g., no internal linking strategy)
- Find content gaps across the site (e.g., missing comparison content)

**TEMPLATE-LEVEL FOCUS:**
- If multiple pages use same template, note this
- Template fixes have exponential impact
- Example: "All product pages (estimated 50+) lack structured data" → HIGH priority

**BUSINESS VALUE:**
- Every recommendation must tie to business outcomes
- Use specific language: "+15% conversion rate" not "better conversions"
- Prioritize by ROI, not just SEO best practices

**SCALABILITY:**
- Prefer fixes that improve many pages at once
- Avoid page-by-page recommendations
- Think: systems, templates, processes

**CONVERSION FOCUS:**
- Analyze user journey across pages
- Identify friction points in funnel
- Assess CTA placement and effectiveness
- Look for trust signals (or lack thereof)

**E-E-A-T ACROSS SITE:**
- Is expertise demonstrated consistently?
- Are there author bios, credentials, case studies?
- Do pages link to each other intelligently?
- Is there a clear brand voice?

**CRITICAL:** This analysis will be used by business owners to make strategic decisions.
Be specific, actionable, and brutally honest about opportunities and problems.
"""

    try:
        ai = AIEngine()

        # Prepare URLs for batch analysis
        urls_to_analyze = [homepage_url] + [page['url'] for page in pages_data]

        # Use URL Context with multiple URLs
        # Note: We'll pass the primary URL and include others in the prompt
        response = ai.analyze_url(
            url=homepage_url,
            prompt=prompt + f"\n\nADDITIONAL PAGES TO ANALYZE: {', '.join(urls_to_analyze[1:])}",
            use_url_context=True
        )

        # Clean and parse JSON response
        cleaned_response = response.strip()

        # Remove markdown code blocks if present
        if cleaned_response.startswith('```json'):
            cleaned_response = cleaned_response.replace('```json', '', 1)
        if cleaned_response.startswith('```'):
            cleaned_response = cleaned_response.replace('```', '', 1)
        if cleaned_response.endswith('```'):
            cleaned_response = cleaned_response.rsplit('```', 1)[0]

        cleaned_response = cleaned_response.strip()

        # Try to find JSON object in response
        if not cleaned_response.startswith('{'):
            start = cleaned_response.find('{')
            end = cleaned_response.rfind('}')
            if start != -1 and end != -1 and end > start:
                cleaned_response = cleaned_response[start:end+1]

        # Parse JSON response
        result = json.loads(cleaned_response)

        # Validate required fields
        required_fields = ['holistic_score', 'template_insights', 'scalable_recommendations']
        for field in required_fields:
            if field not in result:
                return {
                    'success': False,
                    'error': f'AI response missing required field: {field}'
                }

        return {
            'success': True,
            **result
        }

    except json.JSONDecodeError as e:
        print(f"[ERROR] Multi-page JSON Parse Error: {str(e)}")
        print(f"[DEBUG] Raw response (first 500 chars): {response[:500] if 'response' in locals() else 'N/A'}")
        print(f"[DEBUG] Cleaned response (first 500 chars): {cleaned_response[:500] if 'cleaned_response' in locals() else 'N/A'}")
        return {
            'success': False,
            'error': f'Failed to parse AI response as JSON: {str(e)}',
            'raw_response': response[:1000] if 'response' in locals() else ''
        }
    except Exception as e:
        print(f"[ERROR] Holistic AI analysis failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return {
            'success': False,
            'error': f'Holistic AI analysis failed: {str(e)}'
        }


# Test
if __name__ == '__main__':
    print("[TEST] Holistic Multi-Page Analyzer")

    # Mock data
    test_homepage = "https://example.com"
    test_pages = [
        {
            'url': 'https://example.com/products',
            'html': '<html>...</html>',
            'page_type': 'category',
            'selection_reason': 'Shows product taxonomy'
        },
        {
            'url': 'https://example.com/products/laptop',
            'html': '<html>...</html>',
            'page_type': 'product',
            'selection_reason': 'Conversion analysis'
        }
    ]

    result = analyze_site_holistically(
        homepage_url=test_homepage,
        pages_data=test_pages,
        site_type='e-commerce',
        language='en'
    )

    if result['success']:
        print(f"[OK] Holistic score: {result['holistic_score']}/100")
        print(f"[OK] Template insights: {len(result.get('template_insights', []))}")
        print(f"[OK] Scalable recommendations: {len(result.get('scalable_recommendations', []))}")
    else:
        print(f"[ERROR] {result['error']}")
