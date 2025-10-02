# analyzers/ai_content.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ai_engine import AIAnalyzer
from config import GEMINI_API_KEY, ENABLE_AI_ANALYSIS

def analyze_ai_content(url, html_content):
    """
    AI-powered content quality analysis using Gemini 2.5 Flash

    Analyzes:
    - Content quality and depth
    - Search intent match
    - E-E-A-T signals (Experience, Expertise, Authoritativeness, Trust)
    - Content gaps and opportunities
    - Keyword usage naturalness
    """

    results = {
        'score': 0,
        'insights': {},
        'recommendations': [],
        'issues': []
    }

    # Check if AI is enabled
    if not ENABLE_AI_ANALYSIS:
        results['insights']['ai_disabled'] = "AI analysis is disabled in config"
        return results

    # Initialize AI
    try:
        ai = AIAnalyzer(GEMINI_API_KEY)

        if not ai.is_available():
            results['insights']['ai_unavailable'] = "AI not available - check API key"
            return results

    except Exception as e:
        results['insights']['ai_error'] = f"AI initialization failed: {str(e)}"
        return results

    # Prepare prompt for content analysis
    prompt = """
    Analyze this webpage's content quality for SEO purposes.

    Provide a JSON response with this exact structure:
    {
        "content_quality_score": <0-100>,
        "search_intent": {
            "detected_intent": "<informational|transactional|navigational|commercial>",
            "intent_match_score": <0-100>,
            "explanation": "<why this intent was detected>"
        },
        "eeat_signals": {
            "experience_score": <0-100>,
            "expertise_score": <0-100>,
            "authoritativeness_score": <0-100>,
            "trustworthiness_score": <0-100>,
            "findings": ["<signal 1>", "<signal 2>", ...]
        },
        "content_depth": {
            "depth_score": <0-100>,
            "topics_covered": ["<topic 1>", "<topic 2>", ...],
            "missing_topics": ["<gap 1>", "<gap 2>", ...],
            "competitor_advantage": "<what competitors might do better>"
        },
        "keyword_usage": {
            "naturalness_score": <0-100>,
            "keyword_stuffing_detected": <true|false>,
            "primary_keywords": ["<keyword 1>", "<keyword 2>", ...],
            "semantic_keywords": ["<keyword 1>", "<keyword 2>", ...]
        },
        "recommendations": [
            {
                "priority": "<high|medium|low>",
                "category": "<content|structure|keywords|eeat>",
                "title": "<recommendation title>",
                "description": "<detailed explanation>",
                "expected_impact": "<impact description>"
            }
        ]
    }

    Be specific and actionable. Focus on SEO-relevant insights.
    """

    # Analyze with AI
    try:
        response = ai.analyze_url(url, prompt, use_url_context=True)
        analysis = ai.parse_json_response(response)

        if 'error' in analysis:
            results['insights']['ai_error'] = analysis['error']
            return results

        # Parse AI insights
        results['score'] = analysis.get('content_quality_score', 0)
        results['insights'] = {
            'search_intent': analysis.get('search_intent', {}),
            'eeat': analysis.get('eeat_signals', {}),
            'content_depth': analysis.get('content_depth', {}),
            'keyword_usage': analysis.get('keyword_usage', {})
        }

        # Convert recommendations to issues format
        for rec in analysis.get('recommendations', [])[:5]:  # Top 5
            priority_map = {
                'high': ('critical', 9),
                'medium': ('important', 6),
                'low': ('recommendation', 3)
            }
            severity, impact = priority_map.get(rec.get('priority', 'medium'), ('important', 6))

            results['issues'].append({
                'severity': severity,
                'title': f"AI: {rec.get('title', 'Content improvement')}",
                'impact': impact,
                'description': rec.get('description', ''),
                'fix': rec.get('expected_impact', 'Implement this recommendation')
            })

        # Add intent mismatch issue if detected
        intent_data = analysis.get('search_intent', {})
        if intent_data.get('intent_match_score', 100) < 70:
            results['issues'].append({
                'severity': 'important',
                'title': f"AI: Search Intent Mismatch ({intent_data.get('detected_intent', 'unknown')})",
                'impact': 8,
                'description': intent_data.get('explanation', 'Content may not match user search intent'),
                'fix': 'Align content structure and messaging with detected search intent'
            })

        # Add E-E-A-T issues if scores are low
        eeat = analysis.get('eeat_signals', {})
        avg_eeat = sum([
            eeat.get('experience_score', 0),
            eeat.get('expertise_score', 0),
            eeat.get('authoritativeness_score', 0),
            eeat.get('trustworthiness_score', 0)
        ]) / 4

        if avg_eeat < 60:
            results['issues'].append({
                'severity': 'important',
                'title': f"AI: Low E-E-A-T Signals (Score: {avg_eeat:.0f}/100)",
                'impact': 7,
                'description': f"Found signals: {', '.join(eeat.get('findings', [])[:3])}",
                'fix': 'Add author bios, credentials, sources, and trust signals'
            })

        # Add keyword stuffing warning
        kw_usage = analysis.get('keyword_usage', {})
        if kw_usage.get('keyword_stuffing_detected', False):
            results['issues'].append({
                'severity': 'critical',
                'title': 'AI: Keyword Stuffing Detected',
                'impact': 9,
                'description': f"Naturalness score: {kw_usage.get('naturalness_score', 0)}/100",
                'fix': 'Rewrite content to use keywords more naturally and add semantic variations'
            })

    except Exception as e:
        results['insights']['analysis_error'] = str(e)
        print(f"[ERROR] AI Content Analysis Error: {e}")

    return results


# Test function
if __name__ == '__main__':
    test_url = "https://example.com"

    print("Testing AI Content Analyzer...")
    result = analyze_ai_content(test_url, "")

    print(f"\n=== AI CONTENT ANALYSIS ===")
    print(f"Score: {result['score']}/100")
    print(f"\nInsights:")
    for key, value in result['insights'].items():
        print(f"  {key}: {value}")

    print(f"\nIssues Found: {len(result['issues'])}")
    for issue in result['issues']:
        print(f"  [{issue['severity']}] {issue['title']} (Impact: {issue['impact']}/10)")
