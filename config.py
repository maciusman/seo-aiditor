# config.py
import os

# ========================================
# ENVIRONMENT DETECTION
# ========================================

def detect_environment():
    """
    Automatically detect if running in local development or production.

    Returns:
        str: 'local' or 'production'
    """
    # Method 1: Check for config_local.py (local development)
    if os.path.exists(os.path.join(os.path.dirname(__file__), 'config_local.py')):
        return 'local'

    # Method 2: Explicit PRODUCTION environment variable
    if os.getenv('PRODUCTION', '').lower() in ('true', '1', 'yes'):
        return 'production'

    # Method 3: PythonAnywhere detection
    if 'PYTHONANYWHERE_DOMAIN' in os.environ:
        return 'production'

    # Method 4: Other hosting platforms
    if any(key in os.environ for key in ['RENDER', 'RAILWAY_ENVIRONMENT', 'FLY_APP_NAME']):
        return 'production'

    # Default: assume local development
    return 'local'

# Detect current environment
ENV = detect_environment()
IS_PRODUCTION = (ENV == 'production')

# ========================================
# API KEYS CONFIGURATION
# ========================================

if ENV == 'local':
    # Local development: Import from config_local.py
    try:
        from config_local import GOOGLE_PSI_API_KEY, GEMINI_API_KEY
        REQUIRE_USER_API_KEYS = False
        print(f"[CONFIG] Running in LOCAL mode - using config_local.py")
    except ImportError:
        # config_local.py doesn't exist - fallback to environment or placeholders
        GOOGLE_PSI_API_KEY = os.getenv('GOOGLE_PSI_API_KEY', 'YOUR_API_KEY_HERE')
        GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'YOUR_GEMINI_API_KEY_HERE')
        REQUIRE_USER_API_KEYS = False
        print(f"[CONFIG] Warning: config_local.py not found - using environment variables or placeholders")
else:
    # Production: Users must provide their own API keys
    GOOGLE_PSI_API_KEY = None
    GEMINI_API_KEY = None
    REQUIRE_USER_API_KEYS = True
    print(f"[CONFIG] Running in PRODUCTION mode - users must provide API keys")

# Google Gemini API (AI Analysis)
GEMINI_MODEL = "gemini-2.5-flash"  # Model AI
ENABLE_AI_ANALYSIS = True  # Toggle AI features on/off

# Multi-Page Analysis
ENABLE_MULTI_PAGE_ANALYSIS = True  # Enable intelligent multi-page audit
MAX_PAGES_TO_ANALYZE = 5  # Maximum pages per audit (including homepage)
MULTI_PAGE_TIMEOUT = 60  # Total timeout for multi-page analysis (seconds)

# Timeouts
REQUEST_TIMEOUT = 10  # sekundy
PSI_TIMEOUT = 30  # PSI może trwać dłużej

# User agent
USER_AGENT = "SEO-Audit-Tool/1.0 (Educational Purpose)"

# Scoring weights
WEIGHTS = {
    "technical": 0.20,
    "onpage": 0.25,
    "indexing": 0.20,
    "content": 0.20,
    "advanced": 0.15
}

# Thresholds
THRESHOLDS = {
    "title_length_optimal": (50, 60),
    "meta_desc_optimal": (150, 160),
    "page_speed_good": 2500,  # ms
    "word_count_min": 300,
    "word_count_good": 600,
    "keyword_density_optimal": (1, 3)  # %
}
