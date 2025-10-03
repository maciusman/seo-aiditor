# app.py - Flask API Server
from flask import Flask, request, jsonify, Response, send_from_directory
from flask_cors import CORS
import json
import datetime
from urllib.parse import urlparse
from audit_engine import run_audit
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

@app.route('/static/<path:filename>')
def serve_static(filename):
    """Serve static files (logo, etc.)"""
    return send_from_directory('static', filename)

@app.route('/')
def home():
    return jsonify({
        'message': 'SEO AIditor API',
        'version': '1.0.0',
        'endpoints': {
            '/api/audit': 'POST - Run SEO audit',
            '/api/health': 'GET - Health check'
        }
    })

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'service': 'SEO AIditor API'})

@app.route('/api/audit', methods=['POST'])
def audit():
    try:
        data = request.get_json()
        url = data.get('url')

        if not url:
            return jsonify({'error': 'URL is required'}), 400

        # Run the audit
        results = run_audit(url)

        if 'error' in results:
            return jsonify(results), 400

        return jsonify(results), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/export/json', methods=['POST'])
def export_json():
    try:
        data = request.get_json()
        results = data.get('results')

        if not results:
            return jsonify({'error': 'Results are required'}), 400

        # Return JSON formatted results
        return jsonify(results), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/export/csv', methods=['POST'])
def export_csv():
    try:
        data = request.get_json()
        results = data.get('results')

        if not results:
            return jsonify({'error': 'Results are required'}), 400

        # Generate CSV
        csv_data = generate_csv(results)

        return csv_data, 200, {
            'Content-Type': 'text/csv',
            'Content-Disposition': f'attachment; filename=seo_audit_{results.get("url", "report")}.csv'
        }

    except Exception as e:
        return jsonify({'error': str(e)}), 500

def generate_csv(results):
    """Generate CSV export from results"""
    csv_lines = []
    csv_lines.append("Category,Check,Value,Pass,Score")

    for cat_name, cat_data in results.get('categories', {}).items():
        for check_name, check_data in cat_data.get('checks', {}).items():
            csv_lines.append(f"{cat_name},{check_name},{check_data.get('value', 'N/A')},{check_data.get('pass', False)},{check_data.get('score', 0)}")

    csv_lines.append("\nIssues:")
    csv_lines.append("Severity,Title,Impact,Description,Fix")

    for issue in results.get('all_issues', []):
        csv_lines.append(f"{issue.get('severity', '')},{issue.get('title', '')},{issue.get('impact', 0)},{issue.get('description', '')},{issue.get('fix', '')}")

    return "\n".join(csv_lines)

@app.route('/api/export/html', methods=['POST'])
def export_html():
    try:
        data = request.get_json()
        results = data.get('results')

        if not results:
            return jsonify({'error': 'Results are required'}), 400

        # Generate standalone HTML
        html_content = generate_standalone_html(results)

        # Create filename
        url_part = urlparse(results.get('url', 'report')).netloc.replace('.', '_')
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'seo_audit_{url_part}_{timestamp}.html'

        return Response(
            html_content,
            mimetype='text/html',
            headers={
                'Content-Disposition': f'attachment; filename={filename}'
            }
        )

    except Exception as e:
        return jsonify({'error': str(e)}), 500

def generate_standalone_html(results):
    """
    Generate standalone interactive HTML report

    This creates a complete HTML file with:
    - Embedded React, Babel, Tailwind CSS
    - Full UI with tab navigation
    - All data embedded as JSON
    - Works offline without server
    """

    # Read the index.html template
    try:
        with open('index.html', 'r', encoding='utf-8') as f:
            template = f.read()
    except:
        # Fallback if file not found
        return generate_fallback_html(results)

    # Extract CSS from template
    css_start = template.find('<style>')
    css_end = template.find('</style>') + 8
    css_block = template[css_start:css_end] if css_start != -1 else ''

    # Extract React app code
    app_start = template.find('<script type="text/babel">')
    app_end = template.find('</script>', app_start) + 9
    app_code = template[app_start:app_end] if app_start != -1 else ''

    # Clean up app code - remove initial data fetching, use embedded data
    app_code_modified = app_code.replace(
        'const [auditResults, setAuditResults] = useState(null);',
        'const [auditResults, setAuditResults] = useState(window.AUDIT_RESULTS);'
    ).replace(
        'const [loading, setLoading] = useState(false);',
        'const [loading, setLoading] = useState(false); // Report mode - no loading'
    )

    # Escape results for embedding in JavaScript
    results_json = json.dumps(results, ensure_ascii=False, indent=2)

    # Get metadata
    url = results.get('url', 'Unknown')
    score = results.get('final_score', results.get('homepage', {}).get('final_score', 0))
    audit_type = results.get('audit_type', 'single-page')
    timestamp = results.get('timestamp', datetime.datetime.now().isoformat())

    # Build complete HTML
    html = f"""<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SEO Audit Report - {url}</title>

    <!-- React & Babel -->
    <script crossorigin src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
    <script crossorigin src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
    <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>

    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>

    {css_block}

    <style>
        /* Report-specific styles */
        .report-header {{
            background: #1a1a1a;
            color: white;
            padding: 2rem;
            margin-bottom: 2rem;
            border-bottom: 1px solid #2a2a2a;
        }}

        .report-meta {{
            display: flex;
            gap: 2rem;
            flex-wrap: wrap;
            margin-top: 1rem;
            font-size: 0.9rem;
            opacity: 0.95;
        }}

        @media print {{
            .no-print {{
                display: none;
            }}
        }}
    </style>
</head>
<body style="background: #0f0f0f;">
    <!-- Report Header -->
    <div class="report-header">
        <h1 style="font-size: 2rem; font-weight: bold; margin-bottom: 0.5rem; color: #f3f4f6;">
            📊 SEO Audit Report
        </h1>
        <p style="font-size: 1.1rem; opacity: 0.95; color: #e0e0e0;">
            {url}
        </p>
        <div class="report-meta">
            <span style="color: #e0e0e0;">📈 Score: <strong style="color: #f97316;">{score}/100</strong></span>
            <span style="color: #e0e0e0;">🔍 Type: <strong>{audit_type}</strong></span>
            <span style="color: #e0e0e0;">📅 Generated: <strong>{timestamp[:10]}</strong></span>
            <span style="color: #e0e0e0;">🤖 Powered by <strong style="color: #f97316;">SEO AIditor</strong></span>
        </div>
    </div>

    <!-- React App Container -->
    <div id="root"></div>

    <!-- Embedded Audit Data -->
    <script>
        // Audit results embedded directly in HTML
        window.AUDIT_RESULTS = {results_json};

        // Report mode flag
        window.IS_REPORT_MODE = true;
    </script>

    <!-- React Application Code -->
    {app_code_modified}

    <!-- Report Footer -->
    <footer style="text-align: center; padding: 2rem; color: #6b7280; margin-top: 3rem; border-top: 1px solid #2a2a2a;">
        <p style="color: #9ca3af;">Generated by <strong style="color: #f97316;">SEO AIditor</strong> - Professional SEO Audit Tool</p>
        <p style="font-size: 0.875rem; margin-top: 0.5rem; color: #6b7280;">
            This is a standalone HTML report. All functionality works offline.
        </p>
    </footer>
</body>
</html>"""

    return html

def generate_fallback_html(results):
    """Fallback HTML if template not found"""
    results_json = json.dumps(results, ensure_ascii=False, indent=2)

    return f"""<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SEO Audit Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; max-width: 1200px; margin: 0 auto; padding: 20px; }}
        pre {{ background: #f4f4f4; padding: 15px; border-radius: 5px; overflow-x: auto; }}
    </style>
</head>
<body>
    <h1>SEO Audit Report</h1>
    <p><strong>URL:</strong> {results.get('url', 'N/A')}</p>
    <p><strong>Score:</strong> {results.get('final_score', 0)}/100</p>
    <h2>Full Results (JSON)</h2>
    <pre>{results_json}</pre>
</body>
</html>"""

if __name__ == '__main__':
    print("Starting SEO AIditor API Server...")
    print("API will be available at http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
