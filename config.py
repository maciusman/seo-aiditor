# config.py

# Google PageSpeed Insights API
GOOGLE_PSI_API_KEY = "YOUR_API_KEY_HERE"  # Wstaw swój klucz

# Google Gemini API (AI Analysis)
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY_HERE"  # Wstaw swój klucz Gemini
GEMINI_MODEL = "gemini-2.5-flash"  # Model AI
ENABLE_AI_ANALYSIS = True  # Toggle AI features on/off

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
