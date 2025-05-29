"""
Scheduled scraper to run periodically and fetch company data
"""
from django.core.management.base import BaseCommand
from api.scrapers import ScraperManager
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Run scheduled company data fetching from external sources'

    def add_arguments(self, parser):
        parser.add_argument(
            '--sources',
            type=str,
            nargs='+',
            default=['mock', 'opencorporates'],
            help='List of sources to fetch from (space-separated)'
        )
        
        parser.add_argument(
            '--queries',
            type=str,
            nargs='+',
            default=['technology companies', 'startups', 'finance companies'],
            help='List of search queries to use (space-separated)'
        )
        
        parser.add_argument(
            '--limit-per-query',
            type=int,
            default=5,
            help='Maximum companies to fetch per query (default: 5)'
        )

    def handle(self, *args, **options):
        sources = options['sources']
        queries = options['queries']
        limit_per_query = options['limit_per_query']
        
        self.stdout.write(f'Starting scheduled scraper at {datetime.now()}')
        
        scraper_manager = ScraperManager()
        total_companies = 0
        
        for source in sources:
            if source not in scraper_manager.get_available_scrapers():
                self.stdout.write(
                    self.style.WARNING(f'Skipping unknown source: {source}')
                )
                continue
                
            self.stdout.write(f'Processing source: {source}')
            
            for query in queries:
                try:
                    self.stdout.write(f'  Query: "{query}"')
                    companies = scraper_manager.fetch_from_source(
                        source, query, limit_per_query
                    )
                    
                    count = len(companies)
                    total_companies += count
                    
                    self.stdout.write(f'    Fetched: {count} companies')
                    
                    # Brief pause between queries
                    import time
                    time.sleep(2)
                    
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'    Error with query "{query}": {e}')
                    )
                    continue
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Scheduled scraper completed. Total companies processed: {total_companies}'
            )
        )
        
        # Log completion
        logger.info(f'Scheduled scraper completed with {total_companies} companies')
