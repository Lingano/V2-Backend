"""
Django management command to fetch company data from external sources
"""
from django.core.management.base import BaseCommand, CommandError
from api.scrapers import ScraperManager
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Fetch company data from external sources'

    def add_arguments(self, parser):
        parser.add_argument(
            '--source',
            type=str,
            choices=['mock', 'crunchbase', 'opencorporates', 'all'],
            default='all',
            help='Which data source to use (default: all)'
        )
        
        parser.add_argument(
            '--query',
            type=str,
            help='Search query for companies'
        )
        
        parser.add_argument(
            '--limit',
            type=int,
            default=10,
            help='Maximum number of companies to fetch per source (default: 10)'
        )
        
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Fetch data but do not save to database'
        )

    def handle(self, *args, **options):
        source = options['source']
        query = options['query']
        limit = options['limit']
        dry_run = options['dry_run']
        
        if dry_run:
            self.stdout.write(
                self.style.WARNING('Running in dry-run mode - no data will be saved')
            )
        
        scraper_manager = ScraperManager()
        
        try:
            if source == 'all':
                self.stdout.write('Fetching from all available sources...')
                companies = scraper_manager.fetch_from_all_sources(query, limit)
            else:
                self.stdout.write(f'Fetching from {source}...')
                companies = scraper_manager.fetch_from_source(source, query, limit)
            
            if companies:
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Successfully processed {len(companies)} companies'
                    )
                )
                
                # Display summary
                for company in companies:
                    self.stdout.write(f'  - {company.name} ({company.country_of_origin})')
                    
            else:
                self.stdout.write(
                    self.style.WARNING('No companies were fetched or saved')
                )
                
        except Exception as e:
            raise CommandError(f'Error during scraping: {e}')
