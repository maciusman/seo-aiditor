# analyzers/ai_action_plan.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ai_engine import AIAnalyzer
from config import GEMINI_API_KEY, ENABLE_AI_ANALYSIS
import json

def generate_ai_action_plan(url, audit_results):
    """
    AI-powered personalized action plan generator

    Takes full audit results and generates:
    - Prioritized action items
    - Implementation roadmap (30/60/90 days)
    - Expected impact estimates
    - Quick wins identification
    - Resource requirements
    """

    results = {
        'action_plan': {},
        'roadmap': {},
        'quick_wins': [],
        'estimated_impact': {}
    }

    # Check if AI is enabled
    if not ENABLE_AI_ANALYSIS:
        results['error'] = "AI analysis is disabled in config"
        return results

    # Initialize AI
    try:
        ai = AIAnalyzer(GEMINI_API_KEY)

        if not ai.is_available():
            results['error'] = "AI not available - check API key"
            return results

    except Exception as e:
        results['error'] = f"AI initialization failed: {str(e)}"
        return results

    # Prepare audit summary for AI
    audit_summary = {
        'url': url,
        'final_score': audit_results.get('final_score', 0),
        'grade': audit_results.get('grade', {}).get('label', 'UNKNOWN'),
        'category_scores': {
            cat: data.get('score', 0)
            for cat, data in audit_results.get('categories', {}).items()
        },
        'total_issues': len(audit_results.get('all_issues', [])),
        'critical_issues': len([
            i for i in audit_results.get('all_issues', [])
            if i.get('severity') == 'critical'
        ]),
        'top_issues': audit_results.get('all_issues', [])[:10]  # Top 10
    }

    # Detect language from AI content insights
    detected_language = 'en'
    if 'ai_content' in audit_results.get('categories', {}):
        detected_language = audit_results['categories']['ai_content'].get('language', 'en')

    # Language-specific instructions
    lang_instructions = {
        'pl': "Odpowiedz PO POLSKU. Stwórz plan działania w języku polskim.",
        'en': "Respond in ENGLISH. Create action plan in English.",
        'de': "Antworten Sie auf DEUTSCH. Erstellen Sie einen Aktionsplan auf Deutsch.",
        'es': "Responda en ESPAÑOL. Cree un plan de acción en español.",
        'fr': "Répondez en FRANÇAIS. Créez un plan d'action en français."
    }

    lang_instruction = lang_instructions.get(detected_language, lang_instructions['en'])

    # Prepare prompt for action plan
    prompt = f"""{lang_instruction}

You are a senior SEO strategist creating a BATTLE-TESTED action plan for a real client.

CRITICAL: This plan must deliver MEASURABLE business results, not just improve numbers.

AUDIT SUMMARY:
{json.dumps(audit_summary, indent=2)}

**CRITICAL: Your entire response must be ONLY valid JSON. No markdown formatting, no code blocks, no explanations. Start with opening brace and end with closing brace. Pure JSON only.**

Create a JSON response with this EXACT structure:
    {{
        "overall_strategy": {{
            "primary_focus": "<what to focus on first>",
            "estimated_time_to_improvement": "<realistic timeline>",
            "difficulty_level": "<beginner|intermediate|advanced>",
            "required_resources": ["<resource 1>", "<resource 2>", ...]
        }},
        "quick_wins": [
            {{
                "title": "<specific action title>",
                "description": "<what exactly to do>",
                "estimated_time": "<realistic: 15min|30min|1h|2h|4h>",
                "expected_impact": "<be specific: +5% traffic, +10 score points, etc>",
                "business_impact": "<revenue/leads/conversions impact>",
                "difficulty": "<easy|medium|hard>",
                "tools_needed": ["<tool 1>", "<tool 2>"],
                "implementation_steps": ["<step 1 with details>", "<step 2>", ...]
            }}
        ],
        "roadmap_30_days": [
            {{
                "priority": <1-10>,
                "action": "<specific action>",
                "category": "<technical|content|onpage|indexing|conversion>",
                "description": "<what to do and why it matters>",
                "success_criteria": "<measurable KPI: traffic, rankings, conversions>",
                "estimated_impact": "<specific numbers or % if possible>",
                "dependencies": ["<what needs to be done first>"],
                "owner": "<who should do this: developer|marketer|seo|copywriter>"
            }}
        ],
        "roadmap_60_days": [
            {{
                "priority": <1-10>,
                "action": "<specific action>",
                "category": "<category>",
                "description": "<detailed description with business context>",
                "success_criteria": "<measurable outcome>",
                "estimated_impact": "<business impact>",
                "dependencies": ["<prerequisites>"],
                "owner": "<role>"
            }}
        ],
        "roadmap_90_days": [
            {{
                "priority": <1-10>,
                "action": "<strategic action>",
                "category": "<category>",
                "description": "<long-term improvement with reasoning>",
                "success_criteria": "<measurable goal>",
                "estimated_impact": "<cumulative business impact>",
                "dependencies": ["<what must be completed first>"],
                "owner": "<role>"
            }}
        ],
        "estimated_score_progression": {{
            "current": <current score>,
            "after_30_days": <estimated score>,
            "after_60_days": <estimated score>,
            "after_90_days": <estimated score>,
            "assumptions": "<what these estimates assume>"
        }},
        "recommended_tools": [
            {{
                "tool_name": "<tool name>",
                "purpose": "<what it helps with>",
                "cost": "<free|paid|freemium>",
                "priority": "<essential|recommended|optional>"
            }}
        ],
        "content_strategy": {{
            "recommended_content_types": ["<type with reasoning>", ...],
            "keyword_opportunities": ["<keyword with volume estimate>", ...],
            "content_gaps": ["<specific gap with business impact>", ...],
            "competitive_angle": "<unique positioning vs competitors>"
        }},
        "risk_assessment": {{
            "low_hanging_fruit": ["<easy wins with high ROI>"],
            "potential_pitfalls": ["<what could go wrong>"],
            "resource_constraints": ["<likely bottlenecks>"],
            "competitive_threats": ["<what competitors might do>"]
        }},
        "executive_summary": "<2-3 sentences: current state, primary blocker, expected outcome if plan executed>",
        "success_metrics": [
            {{
                "metric": "<specific KPI>",
                "current": "<baseline>",
                "target_30d": "<realistic target>",
                "target_90d": "<ambitious but achievable>"
            }}
        ]
    }}

CRITICAL INSTRUCTIONS:
- Be BRUTALLY HONEST about current state - no sugar coating
- Prioritize by BUSINESS IMPACT, not just SEO metrics
- Every action must have MEASURABLE outcome
- Estimate time/resources REALISTICALLY - no fantasy timelines
- Focus on what will ACTUALLY move the needle for this specific site
- Identify the #1 blocker preventing better rankings
- Think like a business consultant advising on ROI
- Use SPECIFIC numbers whenever possible
- Consider the competitive landscape
- Highlight dependencies and risks
"""

    # Analyze with AI
    try:
        # Use text analysis since we're passing structured data
        response = ai.analyze_text(json.dumps(audit_summary), prompt, json_output=True)
        analysis = ai.parse_json_response(response)

        if 'error' in analysis:
            results['error'] = analysis['error']
            return results

        # Parse AI action plan
        results['action_plan'] = {
            'overall_strategy': analysis.get('overall_strategy', {}),
            'content_strategy': analysis.get('content_strategy', {})
        }

        results['roadmap'] = {
            '30_days': analysis.get('roadmap_30_days', []),
            '60_days': analysis.get('roadmap_60_days', []),
            '90_days': analysis.get('roadmap_90_days', [])
        }

        results['quick_wins'] = analysis.get('quick_wins', [])[:5]  # Top 5

        results['estimated_impact'] = analysis.get('estimated_score_progression', {})

        results['recommended_tools'] = analysis.get('recommended_tools', [])

        # Success message
        results['success'] = True
        results['message'] = f"Generated personalized action plan with {len(results['quick_wins'])} quick wins"

    except Exception as e:
        results['error'] = str(e)
        print(f"[ERROR] AI Action Plan Error: {e}")

    return results


def format_action_plan_for_display(action_plan):
    """
    Format action plan for terminal/UI display

    Returns formatted string
    """
    if 'error' in action_plan:
        return f"[ERROR] Action Plan Error: {action_plan['error']}"

    output = []

    # Header
    output.append("\n" + "="*60)
    output.append("🎯 AI-POWERED PERSONALIZED ACTION PLAN")
    output.append("="*60)

    # Overall Strategy
    strategy = action_plan.get('action_plan', {}).get('overall_strategy', {})
    if strategy:
        output.append("\n📋 OVERALL STRATEGY:")
        output.append(f"  Focus: {strategy.get('primary_focus', 'N/A')}")
        output.append(f"  Timeline: {strategy.get('estimated_time_to_improvement', 'N/A')}")
        output.append(f"  Difficulty: {strategy.get('difficulty_level', 'N/A')}")

    # Quick Wins
    quick_wins = action_plan.get('quick_wins', [])
    if quick_wins:
        output.append("\n⚡ QUICK WINS (High Impact, Low Effort):")
        for i, win in enumerate(quick_wins, 1):
            output.append(f"\n  {i}. {win.get('title', 'N/A')}")
            output.append(f"     Time: {win.get('estimated_time', 'N/A')}")
            output.append(f"     Impact: {win.get('expected_impact', 'N/A')}")

    # Roadmap
    roadmap = action_plan.get('roadmap', {})
    for period, items in [('30_days', '30 Days'), ('60_days', '60 Days'), ('90_days', '90 Days')]:
        tasks = roadmap.get(period, [])
        if tasks:
            output.append(f"\n📅 {items.upper()} ROADMAP:")
            for task in tasks[:3]:  # Top 3 per period
                output.append(f"\n  • {task.get('action', 'N/A')} (Priority: {task.get('priority', 0)}/10)")
                output.append(f"    Impact: {task.get('estimated_impact', 'N/A')}")

    # Estimated Progress
    impact = action_plan.get('estimated_impact', {})
    if impact:
        output.append("\n📊 ESTIMATED SCORE PROGRESSION:")
        output.append(f"  Current: {impact.get('current', 0)}/100")
        output.append(f"  After 30 days: {impact.get('after_30_days', 0)}/100")
        output.append(f"  After 60 days: {impact.get('after_60_days', 0)}/100")
        output.append(f"  After 90 days: {impact.get('after_90_days', 0)}/100")

    output.append("\n" + "="*60)

    return "\n".join(output)


# Test function
if __name__ == '__main__':
    # Mock audit results
    mock_audit = {
        'final_score': 65,
        'grade': {'label': 'NEEDS IMPROVEMENT'},
        'categories': {
            'technical': {'score': 70},
            'onpage': {'score': 60},
            'content': {'score': 55}
        },
        'all_issues': [
            {'severity': 'critical', 'title': 'Missing H1', 'impact': 9},
            {'severity': 'important', 'title': 'Slow LCP', 'impact': 7}
        ]
    }

    print("Testing AI Action Plan Generator...")
    result = generate_ai_action_plan("https://example.com", mock_audit)

    print(format_action_plan_for_display(result))
