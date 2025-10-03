# 📘 SEO AIditor - AI Workflow Documentation

**Wersja:** 2.0
**Model AI:** Google Gemini 2.5 Flash
**Data:** 2025-10-03

---

## 🎯 Spis Treści

1. [Wprowadzenie](#wprowadzenie)
2. [Architektura AI](#architektura-ai)
3. [Single-Page Flow](#single-page-flow)
4. [Multi-Page Flow](#multi-page-flow)
5. [Szczegółowe Prompty](#szczegółowe-prompty)
6. [Struktury JSON Response](#struktury-json-response)
7. [Error Handling](#error-handling)
8. [Jak Usprawnić Prompty](#jak-usprawnić-prompty)

---

## 📋 Wprowadzenie

SEO AIditor wykorzystuje **Google Gemini 2.5 Flash** z **URL Context Tool** do inteligentnej analizy stron internetowych.

### Kluczowe Funkcje AI:
- ✅ **URL Context** - AI pobiera i analizuje strony bezpośrednio (nie trzeba przekazywać HTML)
- ✅ **Multi-Language Support** - auto-detekcja języka (PL, EN, DE, ES, FR)
- ✅ **Holistic Analysis** - analiza wielu stron jako JEDNEJ spójnej witryny
- ✅ **Template-Level Insights** - identyfikacja problemów szablonów (fix 1 = fix N stron)
- ✅ **Business Value Focus** - rekomendacje z wpływem na biznes, nie tylko SEO

### Model: Gemini 2.5 Flash
**Dlaczego Gemini 2.5 Flash?**
- 🚀 Szybki (1-2s na analizę)
- 💰 Tani (0.075$ per 1M tokens input)
- 🌐 URL Context - może sam pobierać strony
- 📊 JSON output - structured responses
- 🔗 Multi-URL batch analysis

---

## 🏗️ Architektura AI

### AI Engine (`ai_engine.py`)

**Klasa:** `AIAnalyzer`

```python
class AIAnalyzer:
    def __init__(self, api_key, model="gemini-2.5-flash"):
        self.tools = [{"url_context": {}}]  # URL Context enabled

    def analyze_url(url, prompt, use_url_context=True):
        """Analizuje URL z pełnym kontekstem strony"""

    def analyze_multiple_urls(urls, prompt):
        """Analizuje wiele URLi razem (holistic)"""

    def analyze_text(text, prompt, json_output=True):
        """Analizuje tekst bez URL Context"""
```

**WAŻNE:**
- Kiedy używamy `tools` (URL Context), **NIE MOŻEMY** użyć `response_mime_type="application/json"`
- Dlatego polegamy na instrukcjach w promptach żeby AI zwróciło JSON
- Dodatkowy JSON parsing czyści markdown (```json, ```)

### Konfiguracja (`config.py`)

```python
GEMINI_API_KEY = "YOUR_KEY"  # z config_local.py
GEMINI_MODEL = "gemini-2.5-flash"
ENABLE_AI_ANALYSIS = True
ENABLE_MULTI_PAGE_ANALYSIS = True
MAX_PAGES_TO_ANALYZE = 5
MULTI_PAGE_TIMEOUT = 60
```

---

## 🔄 Single-Page Flow

### Diagram Przepływu

```
┌─────────────────────────────────────────────────────┐
│  SINGLE-PAGE AUDIT                                  │
├─────────────────────────────────────────────────────┤
│                                                     │
│  1. Homepage Fetch                                  │
│  2. Technical Analysis (non-AI)                     │
│  3. On-Page Analysis (non-AI)                       │
│  4. Indexing Analysis (non-AI)                      │
│  5. Content Analysis (non-AI)                       │
│  6. PageSpeed (Google API)                          │
│  7. ✨ AI Content Analysis (Gemini)                 │
│  8. ✨ AI Action Plan (Gemini)                      │
│                                                     │
│  → Final Score + Issues + Recommendations           │
└─────────────────────────────────────────────────────┘
```

### Krok 7: AI Content Analysis
**Plik:** `analyzers/ai_content.py`
**Funkcja:** `analyze_ai_content(url, html_content)`
**Czas:** ~2-3 sekundy

**Co robi:**
1. Wykrywa język strony
2. Analizuje URL z URL Context
3. Zwraca szczegółową analizę jakości contentu

**Wynik:**
- Content Quality Score (0-100)
- E-E-A-T Analysis (Experience, Expertise, Authoritativeness, Trust)
- Search Intent Match
- Keyword Optimization
- Conversion Optimization
- Business Value Assessment
- Critical Issues + Quick Wins

### Krok 8: AI Action Plan
**Plik:** `analyzers/ai_action_plan.py`
**Funkcja:** `generate_ai_action_plan(url, audit_results)`
**Czas:** ~2-4 sekundy

**Co robi:**
1. Analizuje **pełne wyniki audytu** (wszystkie kategorie + issues)
2. Generuje spersonalizowany plan działania
3. Priorytetyzuje według ROI biznesowego

**Wynik:**
- Overall Strategy
- Quick Wins (5 najlepszych)
- Roadmap (30/60/90 dni)
- Estimated Score Progression
- Recommended Tools
- Success Metrics

---

## 🌐 Multi-Page Flow

### Diagram Przepływu

```
┌──────────────────────────────────────────────────────────────┐
│  MULTI-PAGE AUDIT (Intelligent Site Analysis)               │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  1. Homepage Standard Audit (single-page flow 1-8)           │
│                                                              │
│  ┌────────────────────────────────────────────────────┐     │
│  │  STAGE 1: Site Type Detection & Page Selection    │     │
│  ├────────────────────────────────────────────────────┤     │
│  │  1.1 Crawl homepage → extract links                │     │
│  │  1.2 ✨ AI: Detect site type (e-commerce/service) │     │
│  │  1.3 ✨ AI: Select 4 representative pages          │     │
│  │  1.4 Fetch selected pages in parallel             │     │
│  └────────────────────────────────────────────────────┘     │
│                                                              │
│  ┌────────────────────────────────────────────────────┐     │
│  │  STAGE 2: Holistic AI Analysis                    │     │
│  ├────────────────────────────────────────────────────┤     │
│  │  2.1 ✨ AI: Analyze 5 pages together as ONE site  │     │
│  │  2.2 Template-level insights                      │     │
│  │  2.3 Content patterns across pages                │     │
│  │  2.4 Site-wide strategy                           │     │
│  │  2.5 Scalable recommendations                     │     │
│  │  2.6 Cross-page issues                            │     │
│  │  2.7 Roadmap (week/month/quarter)                 │     │
│  └────────────────────────────────────────────────────┘     │
│                                                              │
│  → Multi-Page Results (homepage + holistic analysis)         │
└──────────────────────────────────────────────────────────────┘
```

### STAGE 1: Site Type Detection & Page Selection

**Plik:** `analyzers/ai_site_structure.py`
**Funkcja:** `detect_site_type_and_select_pages(url, html_content, available_links, language)`
**Czas:** ~10-15 sekund

**Zadanie AI:**
1. **Wykryj typ witryny:** e-commerce, service, blog, corporate, portfolio, news, education, other
2. **Wybierz 4 dodatkowe strony** (oprócz homepage) które najlepiej reprezentują różne aspekty witryny

**Strategia wyboru stron:**
- E-COMMERCE: Category page, Product page, Blog post, About/Trust
- SERVICE: Main service, Secondary service, About/Team, Blog/Resources
- BLOG/NEWS: Recent article, Popular article, Category/Archive, About/Author
- CORPORATE: Products/Solutions, About, Case studies, Contact/CTA

**Kluczowe wymagania:**
- ✅ Strony z **różnych szablonów** (nie 4x product page!)
- ✅ Strony ujawniające **strategię biznesową**
- ✅ Strony pokazujące **conversion funnels**
- ✅ Co najmniej 1 strona contentowa (jeśli dostępna)

**Response JSON:**
```json
{
  "site_type": "e-commerce",
  "site_type_confidence": 95,
  "site_characteristics": {
    "primary_purpose": "Sprzedaż produktów online",
    "target_audience": "Młodzi profesjonaliści 25-40 lat",
    "monetization_model": "E-commerce transactions",
    "content_focus": "Product-focused with lifestyle content"
  },
  "selected_pages": [
    {
      "url": "https://example.com/products/laptops",
      "page_type": "category",
      "selection_reason": "Shows product taxonomy and filtering",
      "expected_insights": "Template structure, internal linking, SEO patterns"
    },
    // ... 3 more pages
  ]
}
```

### STAGE 2: Holistic AI Analysis

**Plik:** `analyzers/ai_multi_page.py`
**Funkcja:** `analyze_site_holistically(homepage_url, pages_data, site_type, language)`
**Czas:** ~30-40 sekund

**Zadanie AI:**
Analizuj **WSZYSTKIE strony razem jako JEDNĄ spójną witrynę**

**KRYTYCZNY MINDSET:**
> "Nie analizuj stron osobno. Szukaj WZORCÓW, SZABLONÓW i problemów SYSTEMOWYCH.
> Myśl: 'Jeśli naprawię ten szablon, ile stron się poprawi?'"

**AI szuka:**
1. **Template-Level Issues** - problemy szablonów (fix 1 = fix N stron)
2. **Content Patterns** - consistency, brand voice, E-E-A-T signals
3. **Site Strategy** - business goals, target audience, value prop
4. **Conversion Funnel** - funnel stages, CTA effectiveness, friction points
5. **Cross-Page Issues** - problemy występujące na wielu stronach
6. **Scalable Recommendations** - rekomendacje skalowalne na całą witrynę

**Response JSON:**
```json
{
  "holistic_score": 75,
  "executive_summary": "Witryna ma solidne fundamenty techniczne...",

  "template_insights": [
    {
      "template_name": "product_page",
      "pages_affected": "~50 stron produktowych",
      "critical_issues": ["Brak structured data", "Słabe opisy meta"],
      "seo_impact": "HIGH",
      "business_impact": "Utrata ~30% potencjalnego trafficu z Google Shopping",
      "fix_difficulty": "MEDIUM",
      "recommended_fix": "Dodaj Product schema markup do szablonu",
      "expected_improvement": "+20-30% CTR w SERP, lepsze pozycje"
    }
  ],

  "content_patterns": {
    "strengths": ["Profesjonalne zdjęcia", "Spójna tonacja"],
    "weaknesses": ["Brak deep content", "Płytkie opisy"],
    "consistency_score": 70,
    "eeat_signals": {
      "experience": 60,
      "expertise": 50,
      "authoritativeness": 45,
      "trustworthiness": 75
    }
  },

  "scalable_recommendations": [
    {
      "category": "TEMPLATE",
      "priority": "CRITICAL",
      "recommendation": "Dodaj FAQ schema do wszystkich stron produktowych",
      "scope": "Dotyczy ~50 stron produktowych",
      "business_impact": "+15% CTR, lepsze featured snippets",
      "implementation_steps": ["Stwórz FAQ component", "Dodaj schema.org FAQ"],
      "time_estimate": "4 hours",
      "owner": "developer"
    }
  ],

  "roadmap": {
    "week_1": ["Fix critical schema markup", "Optimize meta descriptions"],
    "month_1": ["Content depth improvement", "Internal linking strategy"],
    "month_3": ["Blog content expansion", "E-E-A-T signals boost"]
  }
}
```

---

## 📝 Szczegółowe Prompty

### Prompt 1: AI Content Analysis (Single-Page)

**Lokalizacja:** `analyzers/ai_content.py` linia 97

```plaintext
{LANGUAGE_INSTRUCTION}

You are a senior SEO consultant analyzing a client's website.
Provide actionable insights that show REAL BUSINESS VALUE.

Analyze this webpage comprehensively:

URL: {url}

**CRITICAL: Your response MUST be ONLY valid JSON.
No markdown, no explanation, no code blocks. Just pure JSON.**

Provide JSON response with this EXACT structure:
{
    "detected_language": "{detected_lang}",
    "content_quality_score": <0-100, be honest and critical>,
    "page_type": "<homepage|product|article|service|landing|other>",

    "search_intent": {
        "primary_intent": "<informational|transactional|navigational|commercial>",
        "intent_match_score": <0-100>,
        "user_questions_answered": ["<question 1>", "<question 2>", ...],
        "missing_user_questions": ["<what users might ask but page doesn't answer>"],
        "explanation": "<why this intent, with evidence from page>"
    },

    "eeat_analysis": {
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
    },

    "content_depth": {
        "depth_score": <0-100>,
        "depth_level": "<surface|intermediate|comprehensive|expert>",
        "word_count_assessment": "<too short|adequate|comprehensive|too long>",
        "topics_covered": ["<main topic 1>", "<main topic 2>", ...],
        "topics_missing": ["<critical gap 1>", "<critical gap 2>", ...],
        "content_structure_quality": "<poor|fair|good|excellent>",
        "readability_assessment": "<too complex|just right|too simple>",
        "media_usage": "<needs images/videos|adequate|excellent>",
        "competitive_positioning": "<what makes this content unique or generic>"
    },

    "keyword_optimization": {
        "naturalness_score": <0-100>,
        "keyword_stuffing_detected": <true|false>,
        "primary_keywords_found": ["<keyword 1>", "<keyword 2>", ...],
        "semantic_keywords_found": ["<related term 1>", ...],
        "keyword_opportunities": ["<keyword gaps to target>"],
        "keyword_placement_quality": "<poor|fair|good|excellent>",
        "lsi_keywords_present": <true|false>
    },

    "conversion_optimization": {
        "cta_presence": "<none|weak|clear|strong>",
        "cta_examples": ["<CTA text found on page>"],
        "conversion_blockers": ["<what prevents users from converting>"],
        "trust_elements": ["<testimonials, guarantees, etc found>"],
        "urgency_scarcity": "<none|present|overused>",
        "friction_points": ["<what frustrates users>"]
    },

    "business_value_assessment": {
        "target_audience_clarity": <0-100>,
        "value_proposition_clarity": <0-100>,
        "differentiation_strength": <0-100>,
        "monetization_potential": "<low|medium|high>",
        "user_journey_stage": "<awareness|consideration|decision>",
        "business_goal_alignment": "<poor|fair|good|excellent>"
    },

    "critical_issues": [
        {
            "severity": "<critical|high|medium|low>",
            "issue": "<specific problem>",
            "impact": "<business impact in user-friendly terms>",
            "evidence": "<proof from the page>",
            "fix": "<actionable solution>",
            "time_to_fix": "<15min|1h|4h|1day|1week>",
            "expected_improvement": "<what will improve>"
        }
    ],

    "quick_wins": [
        {
            "action": "<specific action to take>",
            "why": "<business reason>",
            "how": "<step-by-step>",
            "time_needed": "<realistic time>",
            "expected_impact": "<traffic increase, conversion uplift, etc>"
        }
    ],

    "competitive_insights": {
        "content_uniqueness": <0-100>,
        "likely_competitors": ["<inferred competitor type>"],
        "competitive_advantages": ["<what this page does well>"],
        "competitive_weaknesses": ["<where competitors likely win>"],
        "differentiation_opportunities": ["<how to stand out>"]
    },

    "overall_summary": "<2-3 sentence executive summary of page quality>",
    "primary_recommendation": "<single most important action to take>",
    "estimated_ranking_potential": "<low|medium|high|very high>"
}

IMPORTANT:
- Be SPECIFIC with examples from the actual page
- Focus on ACTIONABLE insights, not generic advice
- Identify REAL business impact, not just SEO metrics
- Be HONEST about scores - don't inflate
- Provide evidence for every claim
- Think like a business consultant, not just an SEO
```

**Kluczowe elementy:**
- ✅ Language-specific instruction na początku
- ✅ "CRITICAL: Your response MUST be ONLY valid JSON" - wymusza JSON bez markdown
- ✅ Szczegółowa struktura JSON z opisami typów
- ✅ Business value focus - każda metryka z kontekstem biznesowym
- ✅ E-E-A-T analysis - zgodnie z Google guidelines
- ✅ Actionable recommendations - konkretne kroki

### Prompt 2: AI Action Plan (Single-Page)

**Lokalizacja:** `analyzers/ai_action_plan.py` linia 79

```plaintext
{LANGUAGE_INSTRUCTION}

You are a senior SEO strategist creating a BATTLE-TESTED action plan for a real client.

CRITICAL: This plan must deliver MEASURABLE business results, not just improve numbers.

AUDIT SUMMARY:
{json.dumps(audit_summary, indent=2)}

**CRITICAL: Your entire response must be ONLY valid JSON.
No markdown formatting, no code blocks, no explanations.
Start with opening brace and end with closing brace. Pure JSON only.**

Create a JSON response with this EXACT structure:
{
    "overall_strategy": {
        "primary_focus": "<what to focus on first>",
        "estimated_time_to_improvement": "<realistic timeline>",
        "difficulty_level": "<beginner|intermediate|advanced>",
        "required_resources": ["<resource 1>", "<resource 2>", ...]
    },

    "quick_wins": [
        {
            "title": "<specific action title>",
            "description": "<what exactly to do>",
            "estimated_time": "<realistic: 15min|30min|1h|2h|4h>",
            "expected_impact": "<be specific: +5% traffic, +10 score points, etc>",
            "business_impact": "<revenue/leads/conversions impact>",
            "difficulty": "<easy|medium|hard>",
            "tools_needed": ["<tool 1>", "<tool 2>"],
            "implementation_steps": ["<step 1 with details>", "<step 2>", ...]
        }
    ],

    "roadmap_30_days": [
        {
            "priority": <1-10>,
            "action": "<specific action>",
            "category": "<technical|content|onpage|indexing|conversion>",
            "description": "<what to do and why it matters>",
            "success_criteria": "<measurable KPI: traffic, rankings, conversions>",
            "estimated_impact": "<specific numbers or % if possible>",
            "dependencies": ["<what needs to be done first>"],
            "owner": "<who should do this: developer|marketer|seo|copywriter>"
        }
    ],

    "roadmap_60_days": [/* same structure */],
    "roadmap_90_days": [/* same structure */],

    "estimated_score_progression": {
        "current": <current score>,
        "after_30_days": <estimated score>,
        "after_60_days": <estimated score>,
        "after_90_days": <estimated score>,
        "assumptions": "<what these estimates assume>"
    },

    "recommended_tools": [
        {
            "tool_name": "<tool name>",
            "purpose": "<what it helps with>",
            "cost": "<free|paid|freemium>",
            "priority": "<essential|recommended|optional>"
        }
    ],

    "content_strategy": {
        "recommended_content_types": ["<type with reasoning>", ...],
        "keyword_opportunities": ["<keyword with volume estimate>", ...],
        "content_gaps": ["<specific gap with business impact>", ...],
        "competitive_angle": "<unique positioning vs competitors>"
    },

    "risk_assessment": {
        "low_hanging_fruit": ["<easy wins with high ROI>"],
        "potential_pitfalls": ["<what could go wrong>"],
        "resource_constraints": ["<likely bottlenecks>"],
        "competitive_threats": ["<what competitors might do>"]
    },

    "executive_summary": "<2-3 sentences: current state, primary blocker, expected outcome>",

    "success_metrics": [
        {
            "metric": "<specific KPI>",
            "current": "<baseline>",
            "target_30d": "<realistic target>",
            "target_90d": "<ambitious but achievable>"
        }
    ]
}

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
```

**Kluczowe elementy:**
- ✅ Input: pełne wyniki audytu (wszystkie kategorie + issues)
- ✅ Roadmap 30/60/90 dni z dependencies
- ✅ Measurable success criteria dla każdej akcji
- ✅ Owner assignment (developer/marketer/seo/copywriter)
- ✅ Risk assessment - co może pójść źle
- ✅ ROI focus - priorytet według business impact

### Prompt 3: Site Type Detection (Multi-Page Stage 1)

**Lokalizacja:** `analyzers/ai_site_structure.py` linia 51

```plaintext
{LANGUAGE_INSTRUCTION}

**YOUR ROLE:** You are a senior SEO strategist analyzing a website's structure.

**CRITICAL TASK:** Based on the homepage and available internal links, you must:
1. Detect the website type
2. Select 4 ADDITIONAL pages (not homepage) that best represent different aspects of this site

**AVAILABLE INTERNAL LINKS:**
{links_formatted}

**CRITICAL: Your entire response must be ONLY valid JSON
(no markdown, no code blocks, no explanation).**

Start with opening brace and end with closing brace.

**REQUIRED JSON STRUCTURE:**

{
  "site_type": "e-commerce|service|blog|corporate|portfolio|news|education|other",
  "site_type_confidence": 0-100,
  "site_characteristics": {
    "primary_purpose": "string (business goal)",
    "target_audience": "string",
    "monetization_model": "string",
    "content_focus": "string"
  },
  "selected_pages": [
    {
      "url": "full URL from available links",
      "page_type": "category|product|service|about|blog_post|landing|contact|other",
      "selection_reason": "why this page is important for holistic analysis",
      "expected_insights": "what SEO/business insights this page will reveal"
    }
  ]
}

**SELECTION STRATEGY GUIDELINES:**

For E-COMMERCE sites, select:
1. Category page (shows template structure)
2. Product page (conversion optimization)
3. Blog post (content strategy)
4. About/Trust page (E-E-A-T signals)

For SERVICE sites, select:
1. Main service page (value proposition)
2. Secondary service page (breadth analysis)
3. About/Team page (authority signals)
4. Blog/Resources page (content marketing)

For BLOG/NEWS sites, select:
1. Recent article (content quality)
2. Popular/Featured article (best practices)
3. Category/Archive page (structure)
4. About/Author page (E-E-A-T)

For CORPORATE sites, select:
1. Products/Solutions page
2. About/Company page
3. Case studies/Success stories
4. Contact/CTA page

**SELECTION CRITERIA:**
- Choose pages that represent DIFFERENT templates (not 4 product pages!)
- Prioritize pages that reveal business strategy
- Select pages that show conversion funnels
- Include at least one content page (blog/article) if available
- Choose pages likely to have different SEO challenges

**CRITICAL:** You MUST select exactly 4 pages from the available links provided above.
If there are fewer than 4 distinct pages available, select the best ones available
and explain in selection_reason.

**Remember:** This is STAGE 1. These pages will be fetched and analyzed holistically in STAGE 2.
Your selection directly impacts the quality of the final audit.
```

**Kluczowe elementy:**
- ✅ Strategia wyboru stron według typu witryny
- ✅ Wymóg różnorodności szablonów
- ✅ Focus na business strategy & conversion funnels
- ✅ Expected insights - co AI spodziewa się znaleźć
- ✅ Selection reason - uzasadnienie wyboru

### Prompt 4: Holistic Multi-Page Analysis (Stage 2)

**Lokalizacja:** `analyzers/ai_multi_page.py` linia 68

```plaintext
{LANGUAGE_INSTRUCTION}

**YOUR ROLE:** You are a senior SEO & conversion strategist performing
a HOLISTIC multi-page website audit.

**CRITICAL MINDSET:**
You are analyzing ONE WEBSITE, not individual pages.
Look for PATTERNS, TEMPLATES, and SYSTEMIC issues.
Think: "If I fix this template, how many pages improve?"

**WEBSITE TYPE:** {site_type}

**PAGES TO ANALYZE TOGETHER:**
{pages_formatted}

**CRITICAL: Your entire response must be ONLY valid JSON
(no markdown, no code blocks, no explanation).**

Start with opening brace and end with closing brace.

**REQUIRED JSON STRUCTURE:**

{
  "holistic_score": 0-100,
  "executive_summary": "2-3 sentences about overall site health and biggest opportunities",

  "template_insights": [
    {
      "template_name": "e.g., product_page, category_page, blog_post",
      "pages_affected": "approximate number or 'all product pages'",
      "critical_issues": ["issue 1", "issue 2"],
      "seo_impact": "HIGH|MEDIUM|LOW",
      "business_impact": "specific impact on conversions/revenue/leads",
      "fix_difficulty": "EASY|MEDIUM|HARD",
      "recommended_fix": "specific actionable fix",
      "expected_improvement": "quantified outcome if fixed"
    }
  ],

  "content_patterns": {
    "strengths": ["what's working well across pages"],
    "weaknesses": ["systematic content problems"],
    "consistency_score": 0-100,
    "brand_voice_clarity": 0-100,
    "eeat_signals": {
      "experience": 0-100,
      "expertise": 0-100,
      "authoritativeness": 0-100,
      "trustworthiness": 0-100,
      "evidence": ["specific examples from pages"]
    }
  },

  "site_strategy": {
    "primary_business_goal": "inferred from content analysis",
    "target_audience_clarity": 0-100,
    "value_proposition_strength": 0-100,
    "competitive_positioning": "string analysis",
    "content_strategy_assessment": "string analysis",
    "missing_critical_pages": ["pages that should exist but don't"]
  },

  "conversion_funnel": {
    "funnel_stages_present": ["awareness", "consideration", "decision", "action"],
    "funnel_gaps": ["missing stages or weak points"],
    "cta_consistency": 0-100,
    "cta_effectiveness": "analysis of calls-to-action across pages",
    "friction_points": ["obstacles preventing conversion"],
    "quick_conversion_wins": [
      {
        "improvement": "specific change",
        "pages_affected": "which pages",
        "expected_lift": "estimated % improvement",
        "implementation_time": "hours or days"
      }
    ]
  },

  "scalable_recommendations": [
    {
      "category": "TEMPLATE|CONTENT|TECHNICAL|UX",
      "priority": "CRITICAL|HIGH|MEDIUM|LOW",
      "recommendation": "specific action",
      "scope": "affects N pages or entire site",
      "business_impact": "revenue/leads/traffic impact",
      "implementation_steps": ["step 1", "step 2"],
      "time_estimate": "hours/days",
      "owner": "developer|marketer|copywriter|designer",
      "success_metric": "how to measure success"
    }
  ],

  "cross_page_issues": [
    {
      "issue": "problem found across multiple pages",
      "severity": "CRITICAL|HIGH|MEDIUM|LOW",
      "pages_affected": ["list of URLs or 'all pages'"],
      "root_cause": "why this is happening",
      "recommended_solution": "systemic fix"
    }
  ],

  "roadmap": {
    "week_1": ["immediate actions with highest ROI"],
    "month_1": ["foundational improvements"],
    "month_3": ["strategic content & SEO initiatives"],
    "ongoing": ["continuous optimization practices"]
  }
}

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
```

**Kluczowe elementy:**
- ✅ Holistic mindset - ONE website, not separate pages
- ✅ Template-level insights - fix 1 template = fix N pages
- ✅ Business impact quantification - konkretne liczby
- ✅ Scalable recommendations - systemowe rozwiązania
- ✅ Conversion funnel analysis - user journey
- ✅ Cross-page issues - problemy na wielu stronach
- ✅ Roadmap - week/month/quarter prioritization

---

## 📊 Struktury JSON Response

### AI Content Analysis Response

```json
{
  "detected_language": "pl",
  "content_quality_score": 72,
  "page_type": "product",

  "search_intent": {
    "primary_intent": "transactional",
    "intent_match_score": 85,
    "user_questions_answered": [
      "Jakie są specyfikacje produktu?",
      "Ile kosztuje?"
    ],
    "missing_user_questions": [
      "Jak to się ma do konkurencji?",
      "Jakie są opinie użytkowników?"
    ]
  },

  "eeat_analysis": {
    "experience_score": 60,
    "expertise_score": 55,
    "authoritativeness_score": 50,
    "trustworthiness_score": 70,
    "overall_eeat_score": 59,
    "biggest_eeat_weakness": "Brak demonstracji expertise - brak certyfikatów, brak case studies"
  },

  "critical_issues": [
    {
      "severity": "high",
      "issue": "Brak social proof",
      "impact": "Utrata ~25% potencjalnych konwersji",
      "evidence": "Strona nie ma żadnych opinii klientów ani ocen",
      "fix": "Dodaj sekcję z opiniami klientów (minimum 5-10)",
      "time_to_fix": "4h",
      "expected_improvement": "+20-25% conversion rate"
    }
  ],

  "quick_wins": [
    {
      "action": "Dodaj FAQ schema markup",
      "why": "Featured snippets w Google = +30% CTR",
      "how": "Dodaj <script type='application/ld+json'> z FAQ schema",
      "time_needed": "30min",
      "expected_impact": "+15-30% organic CTR"
    }
  ]
}
```

### AI Action Plan Response

```json
{
  "overall_strategy": {
    "primary_focus": "Poprawa E-E-A-T signals i conversion optimization",
    "estimated_time_to_improvement": "30-45 dni na pierwsze rezultaty",
    "difficulty_level": "intermediate",
    "required_resources": ["developer (8h)", "copywriter (16h)", "SEO (4h)"]
  },

  "quick_wins": [
    {
      "title": "Dodaj FAQ schema markup",
      "description": "Dodaj structured data FAQ do 5 najważniejszych stron",
      "estimated_time": "2h",
      "expected_impact": "+20% CTR w SERP dzięki featured snippets",
      "business_impact": "+30-50 dodatkowych sesji/dzień",
      "difficulty": "easy",
      "tools_needed": ["Schema.org validator"],
      "implementation_steps": [
        "Zidentyfikuj 10 najczęstszych pytań klientów",
        "Stwórz FAQ section na kluczowych stronach",
        "Dodaj schema markup zgodnie z schema.org/FAQPage",
        "Przetestuj w Google Rich Results Test"
      ]
    }
  ],

  "roadmap_30_days": [
    {
      "priority": 10,
      "action": "Implementacja structured data na wszystkich stronach produktowych",
      "category": "technical",
      "description": "Dodaj Product schema do szablonu product page...",
      "success_criteria": "100% stron produktowych z validnym schema markup",
      "estimated_impact": "+25% CTR, pojawienie się w Google Shopping",
      "dependencies": ["Audit struktury danych", "Developer availability"],
      "owner": "developer"
    }
  ],

  "estimated_score_progression": {
    "current": 65,
    "after_30_days": 72,
    "after_60_days": 78,
    "after_90_days": 85,
    "assumptions": "Zakładając pełne wdrożenie roadmap i brak większych błędów technicznych"
  }
}
```

### Multi-Page Holistic Response

```json
{
  "holistic_score": 68,
  "executive_summary": "Witryna ma solidną strukturę techniczną ale...",

  "template_insights": [
    {
      "template_name": "product_page",
      "pages_affected": "~50 stron produktowych",
      "critical_issues": [
        "Brak Product schema markup",
        "Meta descriptions za krótkie (30-40 znaków)",
        "Brak internal linkingu do powiązanych produktów"
      ],
      "seo_impact": "HIGH",
      "business_impact": "Utrata ~40% potencjalnego trafficu...",
      "fix_difficulty": "MEDIUM",
      "recommended_fix": "Dodaj Product schema do template...",
      "expected_improvement": "+30-40% CTR, +20% sesji organicznych"
    }
  ],

  "scalable_recommendations": [
    {
      "category": "TEMPLATE",
      "priority": "CRITICAL",
      "recommendation": "Dodaj FAQ schema do wszystkich product pages",
      "scope": "50+ product pages",
      "business_impact": "+25% CTR, featured snippets w 60% queries",
      "implementation_steps": [
        "Stwórz FAQ component w React/Vue",
        "Dodaj schema.org/FAQPage",
        "Deploy do production"
      ],
      "time_estimate": "6 hours",
      "owner": "developer",
      "success_metric": "100% stron z FAQ schema, CTR +20% w 30 dni"
    }
  ],

  "cross_page_issues": [
    {
      "issue": "Wszystkie strony mają identyczne meta descriptions",
      "severity": "HIGH",
      "pages_affected": ["https://example.com/page1", "https://example.com/page2"],
      "root_cause": "Hardcoded meta tag w template zamiast dynamic",
      "recommended_solution": "Zaimplementuj dynamic meta descriptions..."
    }
  ],

  "roadmap": {
    "week_1": [
      "Fix duplicate meta descriptions (CRITICAL)",
      "Add Product schema to top 10 products (QUICK WIN)"
    ],
    "month_1": [
      "Full Product schema rollout",
      "Internal linking strategy implementation"
    ],
    "month_3": [
      "Content expansion (blog)",
      "E-E-A-T signals boost (author bios, case studies)"
    ],
    "ongoing": [
      "Monthly content refresh",
      "Quarterly technical SEO audit"
    ]
  }
}
```

---

## ⚠️ Error Handling

### JSON Parsing Issues

**Problem:** Gemini czasami zwraca JSON w markdown code blocks:

```
```json
{
  "site_type": "e-commerce",
  ...
}
```
```

**Rozwiązanie:** Robust JSON cleaning (`ai_site_structure.py` linia 138):

```python
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
    # Try to find first { and last }
    start = cleaned_response.find('{')
    end = cleaned_response.rfind('}')
    if start != -1 and end != -1 and end > start:
        cleaned_response = cleaned_response[start:end+1]

# Parse JSON response
result = json.loads(cleaned_response)
```

**Debug Logging:**

```python
except json.JSONDecodeError as e:
    print(f"[ERROR] JSON Parse Error: {str(e)}")
    print(f"[DEBUG] Raw response (first 500 chars): {response[:500]}")
    print(f"[DEBUG] Cleaned response (first 500 chars): {cleaned_response[:500]}")
```

### Graceful Fallback (Multi-Page)

**Filozofia:** Multi-page analysis **NIE MOŻE** zepsuć audytu.

**Implementacja (`audit_engine.py` linia 54):**

```python
if enable_multi_page and ENABLE_AI_ANALYSIS:
    try:
        # STAGE 1 & 2
        # ...
        return multi_page_results

    except Exception as e:
        print(f"  ERROR in multi-page analysis: {e}")
        print(f"  Falling back to single-page audit")
        traceback.print_exc()
        return homepage_results  # ← FALLBACK
```

**Punkty fallback:**
1. Crawling fails → return single-page
2. AI site detection fails → return single-page
3. Page fetching fails → return single-page
4. Holistic analysis fails → return single-page

**Rezultat:** Użytkownik ZAWSZE dostaje wyniki, nawet jeśli multi-page się wyłączy.

### URL Context Tool Limitations

**Constraint:** Nie można użyć `response_mime_type="application/json"` gdy używamy `tools` (URL Context)

**Kod (`ai_engine.py` linia 63):**

```python
config_params = {
    'temperature': 0.7,
}

if config_tools:
    config_params['tools'] = config_tools
    # NOTE: response_mime_type cannot be used with tools
else:
    # Only use response_mime_type if NOT using tools
    config_params['response_mime_type'] = "application/json"
```

**Rozwiązanie:** Polegamy na instrukcjach w promptach:
- "Your entire response must be ONLY valid JSON"
- "No markdown, no code blocks, no explanation"
- "Start with opening brace and end with closing brace"

---

## 🚀 Jak Usprawnić Prompty

### 1. A/B Testing Promptów

**Metoda:**
1. Zapisz 2 wersje prompta
2. Uruchom audit na tej samej stronie 5x każdym promptem
3. Porównaj quality i consistency wyników
4. Wybierz lepszy

**Metryki:**
- Consistency - czy AI zwraca spójne wyniki?
- Specificity - czy recommendations są konkretne?
- Actionability - czy można to od razu wdrożyć?
- Business relevance - czy wiąże się z biznesem?

### 2. Few-Shot Examples

**Dodaj przykłady do promptu:**

```plaintext
**EXAMPLE OUTPUT:**
{
  "template_name": "product_page",
  "pages_affected": "~50 product pages",
  "critical_issues": ["Missing Product schema", "Weak meta descriptions"],
  "seo_impact": "HIGH",
  "business_impact": "Loss of ~30% potential Google Shopping traffic",
  ...
}

**NOW ANALYZE THE PROVIDED PAGES:**
```

### 3. Chain of Thought

**Dodaj "Think step-by-step":**

```plaintext
Before providing JSON, think step-by-step:

1. What type of website is this? (evidence: ...)
2. What are the business goals? (evidence: ...)
3. What templates are used? (evidence: ...)
4. What patterns do I see across pages?
5. What's the #1 blocker?

Then provide JSON response:
{...}
```

### 4. Confidence Scores

**Poproś AI o confidence:**

```json
{
  "recommendation": "Add FAQ schema to all product pages",
  "confidence": 95,
  "reasoning": "Based on 50+ similar sites, this consistently gives +20-30% CTR"
}
```

### 5. Iterative Refinement

**Proces:**
1. Uruchom audit
2. Zobacz co AI przegapił
3. Dodaj explicit instruction do prompta
4. Powtórz

**Przykład:**
- AI nie zauważył duplicate content → dodaj "Check for duplicate content across pages"
- AI nie sprawdził canonical tags → dodaj "Verify canonical tag implementation"

### 6. Language-Specific Tuning

**Dla języka polskiego:**

```plaintext
IMPORTANT FOR POLISH LANGUAGE:
- Use informal "Ty" form for recommendations (more actionable)
- Explain technical terms in Polish (e.g., "schema markup" = "znaczniki schema")
- Use Polish business metrics (e.g., "konwersje" not "conversions" in descriptions)
- Consider Polish search behavior (more question-based queries)
```

### 7. Business Context Injection

**Dodaj industry context:**

```plaintext
**INDUSTRY CONTEXT:**
This is an {industry} website.

Common success factors in {industry}:
- {factor 1}
- {factor 2}

Common pitfalls in {industry}:
- {pitfall 1}
- {pitfall 2}

Use this context when analyzing.
```

### 8. Validation Rules

**Dodaj self-check:**

```plaintext
**BEFORE SUBMITTING YOUR RESPONSE, VERIFY:**
- [ ] Every recommendation has estimated business impact
- [ ] Every issue has specific evidence from the page
- [ ] All scores are between 0-100
- [ ] All URLs are from the provided list
- [ ] JSON is valid (no trailing commas, proper quotes)
- [ ] At least 3 quick wins identified
- [ ] Roadmap covers all priority levels
```

### 9. Scoring Rubric

**Standaryzuj scoring:**

```plaintext
**SCORING RUBRIC:**

E-E-A-T Experience (0-100):
- 90-100: First-hand experience clearly demonstrated, personal stories, unique insights
- 70-89: Some experience signals, case studies mentioned
- 50-69: Generic content, limited personal touch
- 30-49: No experience signals
- 0-29: Content appears AI-generated or plagiarized

[Similar rubrics for Expertise, Authoritativeness, Trust]
```

### 10. Output Format Testing

**Test różne formaty:**

```plaintext
# Option A: Detailed explanations
{
  "issue": "Missing H1 tag",
  "why_it_matters": "H1 helps Google understand page topic",
  "impact": "Lower rankings for target keywords",
  ...
}

# Option B: Concise action-oriented
{
  "issue": "Missing H1",
  "fix": "Add <h1>Your Main Keyword</h1> at top",
  "impact": "+5-10 ranking positions",
  ...
}
```

Testuj co działa lepiej dla użytkowników.

---

## 📈 Monitoring & Analytics

### Metryki Jakości Promptów

**Track these metrics:**

1. **JSON Parse Success Rate** - % successful parses
2. **Response Time** - average seconds per analysis
3. **Recommendation Specificity** - % recommendations with numbers
4. **User Action Rate** - % recommendations actually implemented
5. **Business Impact Accuracy** - predicted vs actual impact

### Logging

**Każda analiza AI loguje:**

```python
print(f"[AI] Analyzing {url}...")
print(f"[AI] Detected language: {language}")
print(f"[AI] Content Score: {score}/100")
print(f"[AI] Issues found: {len(issues)}")
print(f"[AI] Quick wins: {len(quick_wins)}")
print(f"[AI] Analysis time: {elapsed}s")
```

### Error Tracking

**Monitor:**
- JSON parse failures
- API timeouts
- Invalid responses
- Fallback triggers

---

## 🎓 Best Practices Summary

### DO ✅
- Używaj URL Context gdy możliwe (szybsze, dokładniejsze)
- Zawsze rób robust JSON parsing (clean markdown)
- Dodawaj language-specific instructions
- Focus na business impact, nie tylko SEO metrics
- Implementuj graceful fallback
- Loguj wszystko (debug, errors, timing)
- Testuj prompty A/B
- Używaj specific examples w promptach

### DON'T ❌
- Nie używaj `response_mime_type` z `tools` (URL Context)
- Nie zakładaj że AI zawsze zwróci valid JSON
- Nie rób page-by-page analysis w multi-page (holistic!)
- Nie używaj generic recommendations
- Nie ignoruj language detection
- Nie skipuj error handling
- Nie trustuj AI blindly - waliduj output

---

## 📞 Support & Contribution

**Jeśli masz pytania lub sugestie dotyczące promptów:**
1. Otwórz issue na GitHub z tagiem `ai-prompts`
2. Opisz problem / sugestię
3. Załącz przykład response (jeśli dotyczy błędu)

**Contributing:**
- Fork repo
- Stwórz branch `feature/improve-{analyzer}-prompt`
- Zmień prompt
- Przetestuj na minimum 5 różnych stronach
- Pull request z metrykami before/after

---

**Ostatnia aktualizacja:** 2025-10-03
**Autor:** SEO AIditor Team
**AI Model:** Gemini 2.5 Flash
**License:** MIT
