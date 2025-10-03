# wsgi.py - Entry point for PythonAnywhere deployment
# This file tells PythonAnywhere how to run your Flask application

import sys
import os

# Add your project directory to the sys.path
# IMPORTANT: Replace 'yourusername' with your actual PythonAnywhere username!
# Example: path = '/home/seoaiditor/seo-aiditor'
path = '/home/yourusername/seo-aiditor'

if path not in sys.path:
    sys.path.append(path)

# Set environment variable to enable production mode
# This tells config.py to require user API keys instead of using config_local.py
os.environ['PRODUCTION'] = 'true'

# Import the Flask app from app.py
from app import app as application

# NOTES:
# 1. Replace 'yourusername' with YOUR PythonAnywhere username
# 2. The variable name MUST be 'application' (not 'app')
# 3. This file is referenced in PythonAnywhere's Web tab -> WSGI configuration
# 4. After any changes to this file, click "Reload" on the Web tab
