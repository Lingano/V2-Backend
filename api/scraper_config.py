"""
Configuration settings for scrapers and external data sources
"""

# API Keys (set these in your environment variables)
SCRAPER_CONFIG = {
    'CRUNCHBASE_API_KEY': None,  # Set via environment variable
    'OPENCORPORATES_API_TOKEN': None,  # Set via environment variable
    
    # Rate limiting settings (seconds between requests)
    'RATE_LIMITS': {
        'default': 1.0,
        'crunchbase': 2.0,
        'opencorporates': 1.5,
        'yellowpages': 2.0,
        'linkedin': 3.0,  # More conservative for LinkedIn
    },
    
    # Default search queries for scheduled scraping
    'DEFAULT_QUERIES': [
        'technology companies',
        'software companies', 
        'fintech startups',
        'healthcare companies',
        'renewable energy companies',
        'artificial intelligence companies',
        'e-commerce companies',
        'biotechnology companies'
    ],
    
    # Countries to focus on
    'TARGET_COUNTRIES': [
        'United States',
        'Canada', 
        'United Kingdom',
        'Germany',
        'France',
        'Japan',
        'Australia',
        'Sweden',
        'Netherlands',
        'Switzerland'
    ],
    
    # Economic sectors mapping
    'SECTOR_MAPPING': {
        'tech': 'Technology',
        'technology': 'Technology',
        'software': 'Technology',
        'ai': 'Technology',
        'artificial intelligence': 'Technology',
        'fintech': 'Finance',
        'finance': 'Finance',
        'banking': 'Finance',
        'health': 'Healthcare',
        'healthcare': 'Healthcare',
        'medical': 'Healthcare',
        'biotech': 'Healthcare',
        'energy': 'Energy',
        'renewable': 'Energy',
        'retail': 'Retail',
        'ecommerce': 'Retail',
        'e-commerce': 'Retail',
        'education': 'Education',
        'manufacturing': 'Manufacturing',
        'automotive': 'Manufacturing',
        'real estate': 'Real Estate',
        'transportation': 'Transportation',
        'logistics': 'Transportation'
    },
    
    # Scraper priorities (higher = run first)
    'SCRAPER_PRIORITIES': {
        'mock': 1,
        'opencorporates': 8,
        'crunchbase': 9,
        'yellowpages': 6,
        'linkedin': 7,
        'crunchbase_web': 5,
    },
    
    # Maximum companies per scraper per run
    'MAX_COMPANIES_PER_SCRAPER': 20,
    
    # Retry settings
    'RETRY_ATTEMPTS': 3,
    'RETRY_DELAY': 5,  # seconds
    
    # User agent strings for web scraping
    'USER_AGENTS': [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    ]
}
