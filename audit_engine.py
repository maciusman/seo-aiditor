# audit_engine.py
import datetime
import re
from bs4 import BeautifulSoup
from utils import validate_url, fetch_url
from analyzers.technical import analyze_technical
from analyzers.onpage import analyze_onpage
from analyzers.indexing import analyze_indexing
from analyzers.content import analyze_content
from analyzers.ai_content import analyze_ai_content, detect_page_language
from analyzers.ai_action_plan import generate_ai_action_plan
# Advanced SEO analyzers (2025)
from analyzers.ai_serp_analysis import analyze_serp_position
from analyzers.ai_intent_analysis import analyze_search_intent_match
from analyzers.ai_eeat_analysis import analyze_eeat_signals
from analyzers.ai_semantic_analysis import analyze_semantic_seo
from analyzers.ai_readability_ux import analyze_readability_ux
from config import WEIGHTS, ENABLE_AI_ANALYSIS, ENABLE_MULTI_PAGE_ANALYSIS, MAX_PAGES_TO_ANALYZE

def extract_primary_keywords(html_content):
    """
    Auto-detect primary keywords from meta title + H1

    Args:
        html_content: Full HTML content

    Returns:
        list: Primary keywords (up to 5)
    """
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        keywords = []

        # Get meta title
        title_tag = soup.find('title')
        if title_tag:
            title_text = title_tag.get_text(strip=True)
            # Extract meaningful words (3+ chars, not common stop words)
            title_words = re.findall(r'\b[a-zA-Z]{3,}\b', title_text.lower())
            keywords.extend(title_words[:3])  # Top 3 from title

        # Get H1
        h1_tag = soup.find('h1')
        if h1_tag:
            h1_text = h1_tag.get_text(strip=True)
            h1_words = re.findall(r'\b[a-zA-Z]{3,}\b', h1_text.lower())
            keywords.extend(h1_words[:2])  # Top 2 from H1

        # Remove duplicates while preserving order
        seen = set()
        unique_keywords = []
        for kw in keywords:
            if kw not in seen and kw not in ['the', 'and', 'for', 'with', 'this', 'that', 'from']:
                seen.add(kw)
                unique_keywords.append(kw)

        return unique_keywords[:5]  # Max 5 keywords

    except Exception as e:
        print(f"  Warning: Could not extract keywords: {e}")
        return ['seo', 'website']  # Fallback

def run_audit(url, multi_page=None, progress_callback=None):
    """
    Uruchom pełny audyt SEO (single-page lub multi-page)

    Args:
        url: Homepage URL
        multi_page: Enable multi-page analysis (None = use config default, True/False = override)
        progress_callback: Optional function(percent, message, details) for progress updates

    Returns:
        dict: Audit results (structure varies based on single/multi-page mode)
    """

    # Helper function to emit progress
    def emit_progress(percent, message, details=None):
        """Emit progress event if callback is provided"""
        print(f"[{percent}%] {message}")  # Console logging
        if progress_callback:
            progress_callback(percent, message, details)

    # Determine if multi-page is enabled
    enable_multi_page = multi_page if multi_page is not None else ENABLE_MULTI_PAGE_ANALYSIS

    # 1. Walidacja URL
    emit_progress(0, "Validating URL...")
    url = validate_url(url)
    if not url:
        return {'error': 'Invalid URL'}

    # 2. Pobierz homepage
    emit_progress(5, f"Fetching homepage: {url}")
    print(f"Fetching {url}...")
    page_data = fetch_url(url)

    if not page_data['success']:
        return {
            'error': 'Cannot fetch page',
            'details': page_data.get('error')
        }

    html_content = page_data['content']

    # Detect language early
    emit_progress(10, "Detecting page language...")
    detected_language = detect_page_language(html_content)
    print(f"  - Detected language: {detected_language}")

    # 3. Run standard single-page audit on homepage
    emit_progress(15, "Analyzing homepage (technical, on-page, content)...")
    print("Running homepage analyzers...")
    homepage_results = run_single_page_audit(url, page_data, html_content, detected_language)

    # 4. If multi-page is enabled, run STAGE 1 & 2
    if enable_multi_page and ENABLE_AI_ANALYSIS:
        print("\n=== MULTI-PAGE ANALYSIS ===")

        try:
            from site_crawler import crawl_homepage, fetch_selected_pages
            from analyzers.ai_site_structure import detect_site_type_and_select_pages
            from analyzers.ai_multi_page import analyze_site_holistically

            # STAGE 1: Crawl homepage & AI selects pages
            emit_progress(35, "Crawling homepage for internal links...")
            print("[STAGE 1] Crawling homepage and detecting site type...")
            crawl_result = crawl_homepage(url)

            if not crawl_result['success']:
                print(f"  Warning: Crawling failed: {crawl_result['error']}")
                print("  Falling back to single-page audit")
                return homepage_results

            available_links = crawl_result['links']
            print(f"  - Found {len(available_links)} internal links")
            emit_progress(40, f"Found {len(available_links)} internal links")

            # AI detects site type and selects pages
            emit_progress(45, "AI analyzing site type and selecting pages...")
            print("[STAGE 1] AI selecting representative pages...")
            selection_result = detect_site_type_and_select_pages(
                url=url,
                html_content=html_content,
                available_links=available_links,
                language=detected_language
            )

            if not selection_result['success']:
                print(f"  Warning: Page selection failed: {selection_result['error']}")
                print("  Falling back to single-page audit")
                return homepage_results

            site_type = selection_result['site_type']
            selected_pages = selection_result['selected_pages'][:MAX_PAGES_TO_ANALYZE - 1]  # -1 for homepage

            print(f"  - Site type: {site_type} (confidence: {selection_result.get('site_type_confidence', 0)}%)")
            print(f"  - Selected {len(selected_pages)} additional pages")
            emit_progress(55, f"Site type: {site_type}. Selected {len(selected_pages)} pages to analyze")

            # STAGE 1.5: Fetch selected pages in parallel
            emit_progress(60, f"Fetching {len(selected_pages)} selected pages...")
            print("[STAGE 1.5] Fetching selected pages in parallel...")
            urls_to_fetch = [page['url'] for page in selected_pages]
            fetched_pages = fetch_selected_pages(urls_to_fetch, timeout_per_page=10)

            successful_pages = [p for p in fetched_pages if p['success']]
            print(f"  - Successfully fetched {len(successful_pages)}/{len(fetched_pages)} pages")
            emit_progress(70, f"Fetched {len(successful_pages)}/{len(fetched_pages)} pages successfully")

            # Merge page data with selection metadata
            pages_for_analysis = []
            for fetched in successful_pages:
                # Find matching selection data
                selection_data = next((p for p in selected_pages if p['url'] == fetched['url']), {})
                pages_for_analysis.append({
                    'url': fetched['url'],
                    'html': fetched['html'],
                    'page_type': selection_data.get('page_type', 'unknown'),
                    'selection_reason': selection_data.get('selection_reason', 'N/A'),
                    'expected_insights': selection_data.get('expected_insights', 'N/A')
                })

            # STAGE 2: Holistic AI analysis
            emit_progress(75, f"Running AI holistic analysis on {len(pages_for_analysis) + 1} pages (30-60s)...")
            print(f"[STAGE 2] AI holistic analysis of {len(pages_for_analysis) + 1} pages (this may take 30-40s)...")
            holistic_result = analyze_site_holistically(
                homepage_url=url,
                pages_data=pages_for_analysis,
                site_type=site_type,
                language=detected_language
            )

            if not holistic_result['success']:
                print(f"  Warning: Holistic analysis failed: {holistic_result['error']}")
                print("  Falling back to single-page audit")
                return homepage_results

            print(f"  - Holistic score: {holistic_result.get('holistic_score', 0)}/100")
            print(f"  - Template insights: {len(holistic_result.get('template_insights', []))}")
            print(f"  - Scalable recommendations: {len(holistic_result.get('scalable_recommendations', []))}")
            emit_progress(90, f"AI analysis complete. Building final results...")

            # 5. Build multi-page response
            multi_page_results = {
                'audit_type': 'multi-page',
                'url': url,
                'timestamp': datetime.datetime.now().isoformat(),
                'language': detected_language,
                'site_type': site_type,
                'site_type_confidence': selection_result.get('site_type_confidence', 0),
                'site_characteristics': selection_result.get('site_characteristics', {}),
                'pages_analyzed': len(pages_for_analysis) + 1,  # +1 for homepage

                # Homepage full audit
                'homepage': homepage_results,

                # Additional pages (AI insights only, no technical crawl)
                'additional_pages': [
                    {
                        'url': page['url'],
                        'page_type': page['page_type'],
                        'selection_reason': page['selection_reason'],
                        'expected_insights': page['expected_insights']
                    }
                    for page in pages_for_analysis
                ],

                # Site-wide holistic analysis
                'site_wide_analysis': holistic_result,

                # Overall scores
                'final_score': homepage_results['final_score'],  # Keep homepage score as primary
                'holistic_score': holistic_result.get('holistic_score', 0),
                'grade': homepage_results['grade']
            }

            emit_progress(100, "Multi-page audit complete!")
            print("\n=== MULTI-PAGE AUDIT COMPLETE ===")
            return multi_page_results

        except Exception as e:
            print(f"  ERROR in multi-page analysis: {e}")
            print(f"  Falling back to single-page audit")
            import traceback
            traceback.print_exc()
            emit_progress(100, "Audit complete (fallback to single-page)")
            return homepage_results

    else:
        # Single-page mode
        if not enable_multi_page:
            print("  Multi-page analysis disabled in config")
        if not ENABLE_AI_ANALYSIS:
            print("  AI analysis disabled (required for multi-page)")

        emit_progress(100, "Single-page audit complete!")
        return homepage_results


def run_single_page_audit(url, page_data, html_content, detected_language='en'):
    """Run standard single-page audit"""

    results = {
        'audit_type': 'single-page',
        'url': url,
        'timestamp': datetime.datetime.now().isoformat(),
        'language': detected_language,
        'categories': {}
    }

    # Technical
    print("  - Technical analysis...")
    results['categories']['technical'] = analyze_technical(url, page_data)

    # On-Page
    print("  - On-page analysis...")
    results['categories']['onpage'] = analyze_onpage(url, html_content)

    # Indexing
    print("  - Indexing analysis...")
    results['categories']['indexing'] = analyze_indexing(url, html_content)

    # Content
    print("  - Content analysis...")
    results['categories']['content'] = analyze_content(html_content)

    # AI Content Analysis (optional, może zająć chwilę)
    if ENABLE_AI_ANALYSIS:
        print("  - AI Content Quality analysis (Gemini 2.5 Flash)...")
        try:
            results['categories']['ai_content'] = analyze_ai_content(url, html_content)
            print(f"    AI Content Score: {results['categories']['ai_content'].get('score', 0)}/100")
        except Exception as e:
            print(f"    Warning: AI Content analysis failed: {e}")
            results['categories']['ai_content'] = {'score': 0, 'error': str(e), 'insights': {}}

        # Advanced SEO Analysis (2025) - 5 AI analyzers
        print("  - Advanced SEO analysis (SERP, Intent, E-E-A-T, Semantic, Readability)...")
        try:
            # Auto-detect primary keywords from meta title + H1
            primary_keywords = extract_primary_keywords(html_content)
            print(f"    Detected keywords: {', '.join(primary_keywords)}")

            advanced_seo = {
                'score': 0,
                'sub_scores': {},
                'insights': {}
            }

            # 1. SERP & Competitive Analysis (with Google Search grounding)
            print("    - SERP & Competitive analysis...")
            try:
                serp_result = analyze_serp_position(url, primary_keywords)
                advanced_seo['sub_scores']['serp'] = serp_result.get('competitive_score', 50)
                advanced_seo['insights']['serp'] = serp_result
            except Exception as e:
                print(f"      Warning: SERP analysis failed: {e}")
                advanced_seo['sub_scores']['serp'] = 50

            # 2. Search Intent Match
            print("    - Search Intent analysis...")
            try:
                intent_result = analyze_search_intent_match(url, html_content, primary_keywords)
                advanced_seo['sub_scores']['intent'] = intent_result.get('intent_score', 50)
                advanced_seo['insights']['intent'] = intent_result
            except Exception as e:
                print(f"      Warning: Intent analysis failed: {e}")
                advanced_seo['sub_scores']['intent'] = 50

            # 3. E-E-A-T Signals (critical for Google 2025)
            print("    - E-E-A-T analysis...")
            try:
                eeat_result = analyze_eeat_signals(url, html_content)
                advanced_seo['sub_scores']['eeat'] = eeat_result.get('overall_eeat_score', 50)
                advanced_seo['insights']['eeat'] = eeat_result
            except Exception as e:
                print(f"      Warning: E-E-A-T analysis failed: {e}")
                advanced_seo['sub_scores']['eeat'] = 50

            # 4. Semantic SEO (entities, topics, LSI)
            print("    - Semantic SEO analysis...")
            try:
                semantic_result = analyze_semantic_seo(html_content, primary_keywords)
                advanced_seo['sub_scores']['semantic'] = semantic_result.get('semantic_score', 50)
                advanced_seo['insights']['semantic'] = semantic_result
            except Exception as e:
                print(f"      Warning: Semantic analysis failed: {e}")
                advanced_seo['sub_scores']['semantic'] = 50

            # 5. Readability & UX
            print("    - Readability & UX analysis...")
            try:
                readability_result = analyze_readability_ux(html_content, target_audience='general')
                advanced_seo['sub_scores']['readability'] = readability_result.get('overall_readability_score', 50)
                advanced_seo['insights']['readability'] = readability_result
            except Exception as e:
                print(f"      Warning: Readability analysis failed: {e}")
                advanced_seo['sub_scores']['readability'] = 50

            # Calculate overall Advanced SEO score (average of 5 sub-scores)
            sub_scores = list(advanced_seo['sub_scores'].values())
            if sub_scores:
                advanced_seo['score'] = round(sum(sub_scores) / len(sub_scores), 1)
            else:
                advanced_seo['score'] = 50

            results['categories']['advanced_seo'] = advanced_seo
            print(f"    Advanced SEO Score: {advanced_seo['score']}/100")

        except Exception as e:
            print(f"    Warning: Advanced SEO analysis failed: {e}")
            results['categories']['advanced_seo'] = {
                'score': 50,
                'error': str(e),
                'sub_scores': {},
                'insights': {}
            }

    else:
        print("  - AI analysis disabled in config")
        results['categories']['ai_content'] = {'score': 0, 'insights': {'disabled': True}}
        results['categories']['advanced_seo'] = {'score': 0, 'insights': {'disabled': True}}

    # Oblicz finalny score
    final_score = calculate_final_score(results['categories'])
    results['final_score'] = final_score
    results['grade'] = get_grade(final_score)

    # Agreguj wszystkie issues
    all_issues = []
    for category in results['categories'].values():
        all_issues.extend(category.get('issues', []))

    # Sortuj po impact (descending)
    all_issues.sort(key=lambda x: x['impact'], reverse=True)
    results['all_issues'] = all_issues

    # Quick wins (high impact, łatwe)
    results['quick_wins'] = [
        issue for issue in all_issues
        if issue['impact'] >= 6 and issue['severity'] in ['important', 'recommendation']
    ][:5]

    # AI Action Plan (personalized recommendations)
    if ENABLE_AI_ANALYSIS:
        print("  - Generating AI Action Plan...")
        try:
            results['ai_action_plan'] = generate_ai_action_plan(url, results)
            if results['ai_action_plan'].get('success'):
                print(f"    [OK] Generated action plan with {len(results['ai_action_plan'].get('quick_wins', []))} AI quick wins")
        except Exception as e:
            print(f"    Warning: AI Action Plan failed: {e}")
            results['ai_action_plan'] = {'error': str(e)}
    else:
        results['ai_action_plan'] = {'disabled': True}

    return results

def calculate_final_score(categories):
    """Oblicz finalny wynik z wagami"""
    score = 0
    score += categories['technical']['score'] * WEIGHTS['technical']
    score += categories['onpage']['score'] * WEIGHTS['onpage']
    score += categories['indexing']['score'] * WEIGHTS['indexing']
    score += categories['content']['score'] * WEIGHTS['content']

    # AI Content score (if available)
    if 'ai_content' in categories and categories['ai_content'].get('score', 0) > 0:
        score += categories['ai_content']['score'] * WEIGHTS.get('ai_content', 0.15)

    # Advanced SEO score (if available)
    if 'advanced_seo' in categories and categories['advanced_seo'].get('score', 0) > 0:
        score += categories['advanced_seo']['score'] * WEIGHTS.get('advanced_seo', 0.20)

    return round(score, 1)

def get_grade(score):
    """Określ ocenę literową"""
    if score >= 90:
        return {'label': 'EXCELLENT', 'color': 'green', 'emoji': '🟢'}
    elif score >= 75:
        return {'label': 'GOOD', 'color': 'lightgreen', 'emoji': '🟡'}
    elif score >= 60:
        return {'label': 'NEEDS IMPROVEMENT', 'color': 'yellow', 'emoji': '🟠'}
    elif score >= 40:
        return {'label': 'POOR', 'color': 'orange', 'emoji': '🔴'}
    else:
        return {'label': 'CRITICAL', 'color': 'red', 'emoji': '⛔'}

# Test
if __name__ == '__main__':
    test_url = "https://example.com"
    result = run_audit(test_url)

    print("\n=== AUDIT RESULTS ===")
    print(f"URL: {result['url']}")
    print(f"Final Score: {result['final_score']}/100 ({result['grade']['label']})")
    print(f"\nCategory Scores:")
    for cat_name, cat_data in result['categories'].items():
        print(f"  {cat_name}: {cat_data['score']:.1f}/100")

    print(f"\nTop Issues:")
    for issue in result['all_issues'][:5]:
        print(f"  [{issue['severity']}] {issue['title']} (Impact: {issue['impact']}/10)")
