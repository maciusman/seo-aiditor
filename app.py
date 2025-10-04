# app.py - Flask API Server
from flask import Flask, request, jsonify, Response, send_from_directory
from flask_cors import CORS
import json
import datetime
from urllib.parse import urlparse
from audit_engine import run_audit
import os
import queue
import threading

app = Flask(__name__, static_folder='static', static_url_path='/static')
CORS(app)  # Enable CORS for frontend communication

@app.route('/logo.png')
def serve_logo():
    """Serve logo from root directory"""
    return send_from_directory('.', 'logo.png')

@app.route('/')
def home():
    """Serve the main frontend application"""
    return send_from_directory('.', 'index.html')

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'service': 'SEO AIditor API'})

@app.route('/api/config', methods=['GET'])
def get_config():
    """
    Returns configuration for frontend to determine if user API keys are required.

    Response:
        {
            'require_user_keys': bool,
            'environment': 'local' | 'production'
        }
    """
    try:
        import config
        return jsonify({
            'require_user_keys': config.REQUIRE_USER_API_KEYS,
            'environment': config.ENV
        })
    except Exception as e:
        # Fallback: If config fails to load, assume production mode
        return jsonify({
            'require_user_keys': True,
            'environment': 'production',
            'error': str(e)
        })

@app.route('/api/audit', methods=['POST'])
def audit():
    try:
        import config
        data = request.get_json()
        url = data.get('url')

        if not url:
            return jsonify({'error': 'URL is required'}), 400

        # Production mode: Accept API keys from user
        if config.REQUIRE_USER_API_KEYS:
            user_gemini_key = data.get('gemini_key')
            user_psi_key = data.get('psi_key', '')

            if not user_gemini_key:
                return jsonify({
                    'error': 'Gemini API key is required. Get your free key at https://aistudio.google.com/apikey'
                }), 400

            # Temporarily set environment variables for this request only
            # Store original values for cleanup
            original_gemini = os.environ.get('GEMINI_API_KEY')
            original_psi = os.environ.get('GOOGLE_PSI_API_KEY')

            try:
                # Set user-provided keys
                os.environ['GEMINI_API_KEY'] = user_gemini_key
                os.environ['GOOGLE_PSI_API_KEY'] = user_psi_key

                # Run the audit with user's keys
                results = run_audit(url)

            finally:
                # Always restore original environment (cleanup)
                if original_gemini is not None:
                    os.environ['GEMINI_API_KEY'] = original_gemini
                elif 'GEMINI_API_KEY' in os.environ:
                    del os.environ['GEMINI_API_KEY']

                if original_psi is not None:
                    os.environ['GOOGLE_PSI_API_KEY'] = original_psi
                elif 'GOOGLE_PSI_API_KEY' in os.environ:
                    del os.environ['GOOGLE_PSI_API_KEY']

        else:
            # Local mode: Use keys from config_local.py
            results = run_audit(url)

        if 'error' in results:
            return jsonify(results), 400

        return jsonify(results), 200

    except Exception as e:
        # Ensure cleanup even on exception
        if config.REQUIRE_USER_API_KEYS:
            if 'original_gemini' in locals() and original_gemini is not None:
                os.environ['GEMINI_API_KEY'] = original_gemini
            if 'original_psi' in locals() and original_psi is not None:
                os.environ['GOOGLE_PSI_API_KEY'] = original_psi

        return jsonify({'error': str(e)}), 500

@app.route('/api/audit-stream', methods=['POST'])
def audit_stream():
    """
    SSE Streaming endpoint for real-time audit progress.

    This endpoint returns Server-Sent Events (SSE) to bypass reverse proxy timeout limits.
    Instead of waiting 120+ seconds for a single response, it sends progress updates
    every few seconds, keeping the connection alive.

    SSE Format:
        data: {"type": "progress", "percent": 25, "message": "Crawling links..."}

        data: {"type": "complete", "results": {...full audit data...}}

    Frontend usage:
        const response = await fetch('/api/audit-stream', {method: 'POST', ...});
        const reader = response.body.getReader();
        // Read stream chunks...
    """

    def generate():
        """Generator function that yields SSE events"""
        import config

        try:
            # Parse request data
            data = request.get_json()
            url = data.get('url')

            if not url:
                yield f"data: {json.dumps({'type': 'error', 'message': 'URL is required'})}\n\n"
                return

            # Production mode: Accept API keys from user
            if config.REQUIRE_USER_API_KEYS:
                user_gemini_key = data.get('gemini_key')
                user_psi_key = data.get('psi_key', '')

                if not user_gemini_key:
                    yield f"data: {json.dumps({'type': 'error', 'message': 'Gemini API key is required'})}\n\n"
                    return

                # Set user-provided keys
                original_gemini = os.environ.get('GEMINI_API_KEY')
                original_psi = os.environ.get('GOOGLE_PSI_API_KEY')

                try:
                    os.environ['GEMINI_API_KEY'] = user_gemini_key
                    os.environ['GOOGLE_PSI_API_KEY'] = user_psi_key

                    # Create a queue for progress events (thread-safe communication)
                    progress_queue = queue.Queue()

                    # Progress callback function - runs in audit thread
                    def progress_callback(percent, message, details=None):
                        """Called by audit_engine to report progress"""
                        event_data = {
                            'type': 'progress',
                            'percent': percent,
                            'message': message
                        }
                        if details:
                            event_data['details'] = details

                        # Put event in queue (thread-safe)
                        progress_queue.put(event_data)

                    # Run audit in separate thread (so we can yield events as they arrive)
                    audit_result = {'data': None, 'error': None}

                    def run_audit_thread():
                        """Thread function to run audit"""
                        try:
                            result = run_audit(url, progress_callback=progress_callback)
                            audit_result['data'] = result
                        except Exception as e:
                            audit_result['error'] = str(e)
                        finally:
                            # Signal completion
                            progress_queue.put({'type': 'DONE'})

                    # Start audit thread
                    thread = threading.Thread(target=run_audit_thread)
                    thread.start()

                    # Initial progress event
                    yield f"data: {json.dumps({'type': 'progress', 'percent': 0, 'message': 'Starting audit...'})}\n\n"

                    # Yield progress events as they arrive in queue
                    while True:
                        try:
                            # Wait for next event (with timeout to prevent hanging)
                            event = progress_queue.get(timeout=1)

                            if event.get('type') == 'DONE':
                                # Audit finished
                                break

                            # Yield progress event
                            yield f"data: {json.dumps(event)}\n\n"

                        except queue.Empty:
                            # No event yet, send keepalive (prevents timeout)
                            yield f": keepalive\n\n"
                            continue

                    # Wait for thread to finish
                    thread.join(timeout=10)

                    # Get final results
                    results = audit_result['data']
                    error = audit_result['error']

                    if error:
                        yield f"data: {json.dumps({'type': 'error', 'message': error})}\n\n"
                        return

                    # Send final results
                    if 'error' in results:
                        yield f"data: {json.dumps({'type': 'error', 'message': results['error']})}\n\n"
                    else:
                        yield f"data: {json.dumps({'type': 'complete', 'results': results})}\n\n"

                finally:
                    # Cleanup environment
                    if original_gemini is not None:
                        os.environ['GEMINI_API_KEY'] = original_gemini
                    elif 'GEMINI_API_KEY' in os.environ:
                        del os.environ['GEMINI_API_KEY']

                    if original_psi is not None:
                        os.environ['GOOGLE_PSI_API_KEY'] = original_psi
                    elif 'GOOGLE_PSI_API_KEY' in os.environ:
                        del os.environ['GOOGLE_PSI_API_KEY']

            else:
                # Local mode - same threading pattern
                progress_queue = queue.Queue()

                def progress_callback(percent, message, details=None):
                    event_data = {
                        'type': 'progress',
                        'percent': percent,
                        'message': message
                    }
                    if details:
                        event_data['details'] = details
                    progress_queue.put(event_data)

                audit_result = {'data': None, 'error': None}

                def run_audit_thread():
                    try:
                        result = run_audit(url, progress_callback=progress_callback)
                        audit_result['data'] = result
                    except Exception as e:
                        audit_result['error'] = str(e)
                    finally:
                        progress_queue.put({'type': 'DONE'})

                thread = threading.Thread(target=run_audit_thread)
                thread.start()

                yield f"data: {json.dumps({'type': 'progress', 'percent': 0, 'message': 'Starting audit...'})}\n\n"

                while True:
                    try:
                        event = progress_queue.get(timeout=1)
                        if event.get('type') == 'DONE':
                            break
                        yield f"data: {json.dumps(event)}\n\n"
                    except queue.Empty:
                        yield f": keepalive\n\n"
                        continue

                thread.join(timeout=10)
                results = audit_result['data']
                error = audit_result['error']

                if error:
                    yield f"data: {json.dumps({'type': 'error', 'message': error})}\n\n"
                elif 'error' in results:
                    yield f"data: {json.dumps({'type': 'error', 'message': results['error']})}\n\n"
                else:
                    yield f"data: {json.dumps({'type': 'complete', 'results': results})}\n\n"

        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"

    # Return SSE response with correct headers
    return Response(
        generate(),
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'X-Accel-Buffering': 'no',  # Disable nginx buffering
            'Connection': 'keep-alive'
        }
    )

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
