from django.core.management.base import BaseCommand
from api.models import Company


class Command(BaseCommand):
    help = 'Demo command to create and retrieve companies'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('=== Company Management Demo ===\n'))
        
        # Create some sample companies
        self.stdout.write('Creating sample companies...')
        
        companies_data = [
            {
                'name': 'TechCorp Solutions',
                'description': 'A leading technology company specializing in software development and cloud services.',
                'country_of_origin': 'United States',
                'economic_sector': 'Technology'
            },
            {
                'name': 'Green Energy Ltd',
                'description': 'Renewable energy company focused on solar and wind power solutions.',
                'country_of_origin': 'Germany',
                'economic_sector': 'Energy'
            },
            {
                'name': 'Global Finance Corp',
                'description': 'International financial services and investment banking.',
                'country_of_origin': 'United Kingdom',
                'economic_sector': 'Finance'
            }
        ]
        
        created_companies = []
        for company_data in companies_data:
            # Check if company already exists
            company, created = Company.objects.get_or_create(
                name=company_data['name'],
                defaults=company_data
            )
            
            if created:
                created_companies.append(company)
                self.stdout.write(f'✓ Created: {company.name}')
            else:
                self.stdout.write(f'⚠ Already exists: {company.name}')
        
        self.stdout.write(f'\nCreated {len(created_companies)} new companies.\n')
        
        # Retrieve and display all companies
        self.stdout.write('=== All Companies in Database ===')
        all_companies = Company.objects.all()
        
        if all_companies:
            for company in all_companies:
                self.stdout.write(f"""
Company ID: {company.id}
Name: {company.name}
Description: {company.description}
Country: {company.country_of_origin}
Sector: {company.economic_sector}
{'-' * 50}""")
        else:
            self.stdout.write('No companies found in database.')
        
        self.stdout.write(f'\nTotal companies in database: {all_companies.count()}')
        
        # Demonstrate filtering
        self.stdout.write('\n=== Filtering Examples ===')
        
        # Filter by country
        us_companies = Company.objects.filter(country_of_origin='United States')
        self.stdout.write(f'Companies from United States: {us_companies.count()}')
        
        # Filter by sector
        tech_companies = Company.objects.filter(economic_sector='Technology')
        self.stdout.write(f'Technology companies: {tech_companies.count()}')
        
        # Search by name containing specific text
        corp_companies = Company.objects.filter(name__icontains='Corp')
        self.stdout.write(f'Companies with "Corp" in name: {corp_companies.count()}')
        
        self.stdout.write(self.style.SUCCESS('\n=== Demo completed successfully! ==='))
