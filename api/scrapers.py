"""
Data scrapers and external data fetchers for the API
"""
import requests
import time
import logging
from typing import List, Dict, Optional
from abc import ABC, abstractmethod
from django.conf import settings
from .models import Company

logger = logging.getLogger(__name__)


class BaseScraper(ABC):
    """Base class for all data scrapers"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    @abstractmethod
    def fetch_data(self, query: str = None, limit: int = 10) -> List[Dict]:
        """Fetch data from external source"""
        pass
    
    def save_companies(self, companies_data: List[Dict]) -> List[Company]:
        """Save scraped company data to database"""
        saved_companies = []
        
        for company_data in companies_data:
            try:
                # Check if company already exists
                existing = Company.objects.filter(
                    name__iexact=company_data.get('name', '')
                ).first()
                
                if existing:
                    # Update existing company
                    for field, value in company_data.items():
                        if hasattr(existing, field) and value:
                            setattr(existing, field, value)
                    existing.save()
                    saved_companies.append(existing)
                    logger.info(f"Updated company: {existing.name}")
                else:
                    # Create new company
                    company = Company.objects.create(**company_data)
                    saved_companies.append(company)
                    logger.info(f"Created new company: {company.name}")
                    
            except Exception as e:
                logger.error(f"Error saving company {company_data.get('name', 'Unknown')}: {e}")
                continue
        
        return saved_companies
    
    def rate_limit(self, delay: float = 1.0):
        """Add delay between requests to be respectful"""
        time.sleep(delay)


class MockAPIScraper(BaseScraper):
    """Mock API scraper for demonstration - fetches from JSONPlaceholder or similar"""
    
    def fetch_data(self, query: str = None, limit: int = 10) -> List[Dict]:
        """Fetch mock company data"""
        try:
            # Using a mock API for demonstration
            url = f"https://jsonplaceholder.typicode.com/users"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            users = response.json()[:limit]
            companies_data = []
            
            for user in users:
                company_data = {
                    'name': user.get('company', {}).get('name', f"{user['name']} Corp"),
                    'description': user.get('company', {}).get('catchPhrase', 'A innovative company'),
                    'country_of_origin': user.get('address', {}).get('city', 'Unknown'),
                    'economic_sector': self._get_random_sector()
                }
                companies_data.append(company_data)
                
            return companies_data
            
        except Exception as e:
            logger.error(f"Error fetching from Mock API: {e}")
            return []
    
    def _get_random_sector(self) -> str:
        """Get a random economic sector"""
        sectors = [
            'Technology', 'Finance', 'Healthcare', 'Manufacturing', 
            'Retail', 'Energy', 'Transportation', 'Education'
        ]
        import random
        return random.choice(sectors)


class CrunchbaseScraper(BaseScraper):
    """Scraper for Crunchbase-like data (requires API key in production)"""
    
    def __init__(self):
        super().__init__()
        self.api_key = getattr(settings, 'CRUNCHBASE_API_KEY', None)
        self.base_url = "https://api.crunchbase.com/api/v4"
    
    def fetch_data(self, query: str = None, limit: int = 10) -> List[Dict]:
        """Fetch company data from Crunchbase API"""
        if not self.api_key:
            logger.warning("Crunchbase API key not configured, using mock data")
            return self._get_mock_crunchbase_data(limit)
        
        try:
            # This would be the actual Crunchbase API call
            # headers = {'X-cb-user-key': self.api_key}
            # response = self.session.get(f"{self.base_url}/searches/organizations", 
            #                           headers=headers, params={'query': query})
            
            # For now, return mock data
            return self._get_mock_crunchbase_data(limit)
            
        except Exception as e:
            logger.error(f"Error fetching from Crunchbase: {e}")
            return []
    
    def _get_mock_crunchbase_data(self, limit: int) -> List[Dict]:
        """Generate mock company data in Crunchbase style"""
        mock_companies = [
            {
                'name': 'TechNova Solutions',
                'description': 'AI-powered software solutions for enterprise clients',
                'country_of_origin': 'United States',
                'economic_sector': 'Technology'
            },
            {
                'name': 'GreenEnergy Corp',
                'description': 'Renewable energy solutions and sustainable technology',
                'country_of_origin': 'Germany',
                'economic_sector': 'Energy'
            },
            {
                'name': 'HealthTech Innovations',
                'description': 'Digital health platforms and medical device manufacturing',
                'country_of_origin': 'Canada',
                'economic_sector': 'Healthcare'
            },
            {
                'name': 'FinanceFlow Ltd',
                'description': 'Fintech solutions for digital banking and payments',
                'country_of_origin': 'United Kingdom',
                'economic_sector': 'Finance'
            },
            {
                'name': 'EduLearn Platform',
                'description': 'Online learning management and educational technology',
                'country_of_origin': 'Australia',
                'economic_sector': 'Education'
            }
        ]
        
        return mock_companies[:limit]


class OpenCorporatesScraper(BaseScraper):
    """Scraper for OpenCorporates data (free tier available)"""
    
    def __init__(self):
        super().__init__()
        self.base_url = "https://api.opencorporates.com/v0.4"
        self.api_token = getattr(settings, 'OPENCORPORATES_API_TOKEN', None)
    
    def fetch_data(self, query: str = None, limit: int = 10) -> List[Dict]:
        """Fetch company data from OpenCorporates"""
        try:
            params = {
                'q': query or 'company',
                'per_page': min(limit, 30),  # API limit
                'format': 'json'
            }
            
            if self.api_token:
                params['api_token'] = self.api_token
            
            response = self.session.get(
                f"{self.base_url}/companies/search",
                params=params,
                timeout=15
            )
            
            if response.status_code == 200:
                data = response.json()
                companies_data = []
                
                for company in data.get('results', {}).get('companies', []):
                    company_info = company.get('company', {})
                    company_data = {
                        'name': company_info.get('name', 'Unknown Company'),
                        'description': f"Company from {company_info.get('jurisdiction_code', 'Unknown')}",
                        'country_of_origin': self._get_country_from_jurisdiction(
                            company_info.get('jurisdiction_code', '')
                        ),
                        'economic_sector': company_info.get('company_type', 'Unknown')
                    }
                    companies_data.append(company_data)
                
                return companies_data
            else:
                logger.warning(f"OpenCorporates API returned status {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"Error fetching from OpenCorporates: {e}")
            return []
    
    def _get_country_from_jurisdiction(self, jurisdiction_code: str) -> str:
        """Convert jurisdiction code to country name"""
        jurisdiction_map = {
            'us_': 'United States',
            'gb': 'United Kingdom', 
            'ca_': 'Canada',
            'de': 'Germany',
            'fr': 'France',
            'au_': 'Australia',
            'jp': 'Japan'
        }
        
        for code, country in jurisdiction_map.items():
            if jurisdiction_code.lower().startswith(code):
                return country
        
        return 'Unknown'


class ScraperManager:
    """Manager class to coordinate different scrapers"""
    
    def __init__(self):
        self.scrapers = {
            'mock': MockAPIScraper(),
            'crunchbase': CrunchbaseScraper(),
            'opencorporates': OpenCorporatesScraper(),
        }
        
        # Import web scrapers dynamically to avoid circular imports
        try:
            from .web_scrapers import YellowPagesScraper, LinkedInCompaniesScraper, CrunchbaseWebScraper
            self.scrapers.update({
                'yellowpages': YellowPagesScraper(),
                'linkedin': LinkedInCompaniesScraper(),
                'crunchbase_web': CrunchbaseWebScraper(),
            })
        except ImportError as e:
            logger.warning(f"Could not import web scrapers: {e}")
    
    def get_scraper(self, scraper_type: str) -> Optional[BaseScraper]:
        """Get a specific scraper by type"""
        return self.scrapers.get(scraper_type)
    
    def get_available_scrapers(self) -> List[str]:
        """Get list of available scraper types"""
        return list(self.scrapers.keys())
    
    def fetch_from_all_sources(self, query: str = None, limit_per_source: int = 5) -> List[Company]:
        """Fetch data from all available scrapers"""
        all_companies = []
        
        for scraper_name, scraper in self.scrapers.items():
            try:
                logger.info(f"Fetching data from {scraper_name}")
                companies_data = scraper.fetch_data(query, limit_per_source)
                saved_companies = scraper.save_companies(companies_data)
                all_companies.extend(saved_companies)
                
                # Rate limiting between different sources
                scraper.rate_limit(2.0)
                
            except Exception as e:
                logger.error(f"Error with {scraper_name} scraper: {e}")
                continue
        
        return all_companies
    
    def fetch_from_source(self, source: str, query: str = None, limit: int = 10) -> List[Company]:
        """Fetch data from a specific source"""
        scraper = self.get_scraper(source)
        if not scraper:
            raise ValueError(f"Unknown scraper source: {source}. Available: {self.get_available_scrapers()}")
        
        companies_data = scraper.fetch_data(query, limit)
        return scraper.save_companies(companies_data)
