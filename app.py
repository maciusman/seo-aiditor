# app.py - Flask API Server
from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from audit_engine import run_audit

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

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

if __name__ == '__main__':
    print("Starting SEO AIditor API Server...")
    print("API will be available at http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
