# analyzers/ai_content_v2.py - Enhanced AI Content Analysis
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ai_engine import AIAnalyzer
from config import GEMINI_API_KEY, ENABLE_AI_ANALYSIS
from bs4 import BeautifulSoup
import json

def detect_page_language(html_content):
    """Detect page language from HTML"""
    try:
        soup = BeautifulSoup(html_content, 'html.parser')

        # Check lang attribute
        html_tag = soup.find('html')
        if html_tag and html_tag.get('lang'):
            lang = html_tag.get('lang')[:2].lower()
            return lang

        # Check meta content-language
        meta_lang = soup.find('meta', attrs={'http-equiv': 'content-language'})
        if meta_lang and meta_lang.get('content'):
            return meta_lang.get('content')[:2].lower()

        # Default to detecting from content
        text_sample = soup.get_text()[:500]

        # Simple heuristics
        polish_indicators = ['jest', 'się', 'nie', 'czy', 'jak', 'który', 'dla']
        english_indicators = ['the', 'is', 'are', 'and', 'for', 'with', 'that']

        polish_count = sum(1 for word in polish_indicators if word in text_sample.lower())
        english_count = sum(1 for word in english_indicators if word in text_sample.lower())

        if polish_count > english_count:
            return 'pl'
        return 'en'

    except:
        return 'en'

def analyze_ai_content(url, html_content):
    """
    Enhanced AI-powered content quality analysis

    NEW FEATURES:
    - Auto language detection
    - Deeper E-E-A-T analysis
    - Competitive positioning
    - Conversion optimization hints
    - Business value assessment
    """

    results = {
        'score': 0,
        'insights': {},
        'recommendations': [],
        'issues': [],
        'language': 'unknown'
    }

    # Check if AI is enabled
    if not ENABLE_AI_ANALYSIS:
        results['insights']['ai_disabled'] = "AI analysis is disabled in config"
        return results

    # Detect language
    detected_lang = detect_page_language(html_content)
    results['language'] = detected_lang
    print(f"[AI] Detected language: {detected_lang}")

    # Initialize AI
    try:
        ai = AIAnalyzer(GEMINI_API_KEY)

        if not ai.is_available():
            results['insights']['ai_unavailable'] = "AI not available - check API key"
            return results

    except Exception as e:
        results['insights']['ai_error'] = f"AI initialization failed: {str(e)}"
        return results

    # Language-specific instructions
    lang_instructions = {
        'pl': "Odpowiedz PO POLSKU. Analizuj treść w języku polskim.",
        'en': "Respond in ENGLISH. Analyze content in English.",
        'de': "Antworten Sie auf DEUTSCH. Analysieren Sie Inhalte auf Deutsch.",
        'es': "Responda en ESPAÑOL. Analice el contenido en español.",
        'fr': "Répondez en FRANÇAIS. Analysez le contenu en français."
    }

    lang_instruction = lang_instructions.get(detected_lang, lang_instructions['en'])

    # Enhanced prompt with more business value
    prompt = f"""{lang_instruction}

You are a senior SEO consultant analyzing a client's website. Provide actionable insights that show REAL BUSINESS VALUE.

Analyze this webpage comprehensively:

URL: {url}

**CRITICAL: Your response MUST be ONLY valid JSON. No markdown, no explanation, no code blocks. Just pure JSON.**

Provide JSON response with this EXACT structure:
{{
    "detected_language": "{detected_lang}",
    "content_quality_score": <0-100, be honest and critical>,
    "page_type": "<homepage|product|article|service|landing|other>",

    "search_intent": {{
        "primary_intent": "<informational|transactional|navigational|commercial>",
        "intent_match_score": <0-100>,
        "user_questions_answered": ["<question 1>", "<question 2>", ...],
        "missing_user_questions": ["<what users might ask but page doesn't answer>"],
        "explanation": "<why this intent, with evidence from page>"
    }},

    "eeat_analysis": {{
        "experience_score": <0-100>,
        "experience_signals": ["<specific examples from page>"],
        "expertise_score": <0-100>,
        "expertise_signals": ["<credentials, data, depth found>"],
        "authoritativeness_score": <0-100>,
        "authority_signals": ["<links, mentions, social proof>"],
        "trustworthiness_score": <0-100>,
        "trust_signals": ["<contact info, transparency, security>"],
        "overall_eeat_score": <average of 4 scores>,
        "biggest_eeat_weakness": "<what hurts E-E-A-T most>",
        "quick_eeat_wins": ["<easy fixes to improve E-E-A-T>"]
    }},

    "content_depth": {{
        "depth_score": <0-100>,
        "depth_level": "<surface|intermediate|comprehensive|expert>",
        "word_count_assessment": "<too short|adequate|comprehensive|too long>",
        "topics_covered": ["<main topic 1>", "<main topic 2>", ...],
        "topics_missing": ["<critical gap 1>", "<critical gap 2>", ...],
        "content_structure_quality": "<poor|fair|good|excellent>",
        "readability_assessment": "<too complex|just right|too simple>",
        "media_usage": "<needs images/videos|adequate|excellent>",
        "competitive_positioning": "<what makes this content unique or generic>"
    }},

    "keyword_optimization": {{
        "naturalness_score": <0-100>,
        "keyword_stuffing_detected": <true|false>,
        "primary_keywords_found": ["<keyword 1>", "<keyword 2>", ...],
        "semantic_keywords_found": ["<related term 1>", ...],
        "keyword_opportunities": ["<keyword gaps to target>"],
        "keyword_placement_quality": "<poor|fair|good|excellent>",
        "lsi_keywords_present": <true|false>
    }},

    "conversion_optimization": {{
        "cta_presence": "<none|weak|clear|strong>",
        "cta_examples": ["<CTA text found on page>"],
        "conversion_blockers": ["<what prevents users from converting>"],
        "trust_elements": ["<testimonials, guarantees, etc found>"],
        "urgency_scarcity": "<none|present|overused>",
        "friction_points": ["<what frustrates users>"]
    }},

    "business_value_assessment": {{
        "target_audience_clarity": <0-100>,
        "value_proposition_clarity": <0-100>,
        "differentiation_strength": <0-100>,
        "monetization_potential": "<low|medium|high>",
        "user_journey_stage": "<awareness|consideration|decision>",
        "business_goal_alignment": "<poor|fair|good|excellent>"
    }},

    "critical_issues": [
        {{
            "severity": "<critical|high|medium|low>",
            "issue": "<specific problem>",
            "impact": "<business impact in user-friendly terms>",
            "evidence": "<proof from the page>",
            "fix": "<actionable solution>",
            "time_to_fix": "<15min|1h|4h|1day|1week>",
            "expected_improvement": "<what will improve>"
        }}
    ],

    "quick_wins": [
        {{
            "action": "<specific action to take>",
            "why": "<business reason>",
            "how": "<step-by-step>",
            "time_needed": "<realistic time>",
            "expected_impact": "<traffic increase, conversion uplift, etc>"
        }}
    ],

    "competitive_insights": {{
        "content_uniqueness": <0-100>,
        "likely_competitors": ["<inferred competitor type>"],
        "competitive_advantages": ["<what this page does well>"],
        "competitive_weaknesses": ["<where competitors likely win>"],
        "differentiation_opportunities": ["<how to stand out>"]
    }},

    "overall_summary": "<2-3 sentence executive summary of page quality>",
    "primary_recommendation": "<single most important action to take>",
    "estimated_ranking_potential": "<low|medium|high|very high>"
}}

IMPORTANT:
- Be SPECIFIC with examples from the actual page
- Focus on ACTIONABLE insights, not generic advice
- Identify REAL business impact, not just SEO metrics
- Be HONEST about scores - don't inflate
- Provide evidence for every claim
- Think like a business consultant, not just an SEO
"""

    # Analyze with AI (with retry)
    try:
        print(f"[AI] Analyzing content for {url}...")
        response = ai.analyze_with_retry(url, prompt, max_retries=2)

        if 'error' in response:
            results['insights']['ai_error'] = response['error']
            print(f"[ERROR] AI analysis failed: {response['error']}")
            return results

        # Parse AI insights
        results['score'] = response.get('content_quality_score', 0)
        results['insights'] = {
            'page_type': response.get('page_type', 'unknown'),
            'search_intent': response.get('search_intent', {}),
            'eeat': response.get('eeat_analysis', {}),
            'content_depth': response.get('content_depth', {}),
            'keywords': response.get('keyword_optimization', {}),
            'conversion': response.get('conversion_optimization', {}),
            'business_value': response.get('business_value_assessment', {}),
            'competitive': response.get('competitive_insights', {}),
            'summary': response.get('overall_summary', ''),
            'primary_recommendation': response.get('primary_recommendation', '')
        }

        # Convert critical issues to standard format
        for issue in response.get('critical_issues', [])[:5]:
            severity_map = {
                'critical': ('critical', 10),
                'high': ('critical', 9),
                'medium': ('important', 6),
                'low': ('recommendation', 3)
            }
            severity, impact = severity_map.get(issue.get('severity', 'medium'), ('important', 6))

            results['issues'].append({
                'severity': severity,
                'title': f"AI: {issue.get('issue', 'Content issue')}",
                'impact': impact,
                'description': f"{issue.get('evidence', '')} Impact: {issue.get('impact', '')}",
                'fix': f"{issue.get('fix', '')} (Time: {issue.get('time_to_fix', 'unknown')})"
            })

        # Add quick wins as issues
        for win in response.get('quick_wins', [])[:3]:
            results['issues'].append({
                'severity': 'recommendation',
                'title': f"AI Quick Win: {win.get('action', 'Optimization')}",
                'impact': 8,
                'description': f"Why: {win.get('why', '')}",
                'fix': f"{win.get('how', '')} Expected: {win.get('expected_impact', '')}"
            })

        print(f"[OK] AI Content Analysis complete - Score: {results['score']}/100")

    except Exception as e:
        results['insights']['analysis_error'] = str(e)
        print(f"[ERROR] AI Content Analysis Error: {e}")

    return results


# Test function
if __name__ == '__main__':
    import requests

    test_url = input("Enter URL to test (or press Enter for example.com): ").strip()
    if not test_url:
        test_url = "https://example.com"

    print(f"\n[TEST] Fetching {test_url}...")
    try:
        response = requests.get(test_url, timeout=10)
        html_content = response.text

        print("[TEST] Running AI Content Analysis...")
        result = analyze_ai_content(test_url, html_content)

        print(f"\n=== AI CONTENT ANALYSIS ===")
        print(f"Language: {result['language']}")
        print(f"Score: {result['score']}/100")
        print(f"\nPage Type: {result['insights'].get('page_type', 'unknown')}")
        print(f"\nSummary: {result['insights'].get('summary', 'N/A')}")
        print(f"\nPrimary Recommendation: {result['insights'].get('primary_recommendation', 'N/A')}")

        print(f"\nIssues Found: {len(result['issues'])}")
        for issue in result['issues'][:3]:
            print(f"  [{issue['severity']}] {issue['title']}")
            print(f"     {issue['description'][:100]}...")

    except Exception as e:
        print(f"[ERROR] Test failed: {e}")
