# wsgi.py - Entry point for production deployment (Gunicorn/uWSGI)
# This file works for: Mikr.us VPS, DigitalOcean, AWS, Render, Railway, etc.

import sys
import os

# Add your project directory to the sys.path
# For Mikr.us VPS: /var/www/seo-aiditor
# For PythonAnywhere: /home/yourusername/seo-aiditor
path = '/var/www/seo-aiditor'

if path not in sys.path:
    sys.path.append(path)

# Set environment variable to enable production mode
# This tells config.py to require user API keys instead of using config_local.py
os.environ['PRODUCTION'] = 'true'

# Import the Flask app from app.py
from app import app as application

if __name__ == "__main__":
    # This runs only for direct execution (python wsgi.py)
    # Gunicorn/uWSGI will use 'application' directly
    application.run()

# DEPLOYMENT NOTES:
#
# Mikr.us VPS (Gunicorn):
#   gunicorn --bind 0.0.0.0:5000 wsgi:app
#
# PythonAnywhere:
#   1. Change path to: /home/yourusername/seo-aiditor
#   2. Configure in Web tab -> WSGI configuration
#
# After changes: Restart your WSGI server (systemctl restart / Reload button)
