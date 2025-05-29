"""
Django ORM demonstration script for Company model
This script shows how to create and retrieve Company models using Django ORM directly
"""

import os
import sys
import django

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from api.models import Company

def create_sample_companies():
    """Create sample companies using Django ORM"""
    print("=== Creating Sample Companies ===\n")
    
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
        },
        {
            'name': 'Local Manufacturing Inc',
            'description': 'Manufacturing company producing consumer goods.',
            'country_of_origin': 'Canada',
            'economic_sector': 'Manufacturing'
        }
    ]
    
    created_count = 0
    for company_data in companies_data:
        # Check if company already exists
        company, created = Company.objects.get_or_create(
            name=company_data['name'],
            defaults=company_data
        )
        
        if created:
            print(f"✓ Created: {company.name}")
            created_count += 1
        else:
            print(f"⚠ Already exists: {company.name}")
    
    print(f"\nCreated {created_count} new companies.\n")
    return created_count

def retrieve_and_display_companies():
    """Retrieve and display all companies"""
    print("=== All Companies in Database ===\n")
    
    companies = Company.objects.all()
    
    if companies.exists():
        for company in companies:
            print(f"""
ID: {company.id}
Name: {company.name}
Description: {company.description}
Country: {company.country_of_origin}
Sector: {company.economic_sector}
{'-' * 60}""")
    else:
        print("No companies found in database.")
    
    print(f"Total companies: {companies.count()}\n")
    return companies

def demonstrate_filtering():
    """Demonstrate different ways to filter companies"""
    print("=== Filtering and Querying Examples ===\n")
    
    # Filter by country
    us_companies = Company.objects.filter(country_of_origin='United States')
    print(f"Companies from United States: {us_companies.count()}")
    for company in us_companies:
        print(f"  - {company.name}")
    
    # Filter by sector
    tech_companies = Company.objects.filter(economic_sector='Technology')
    print(f"\nTechnology companies: {tech_companies.count()}")
    for company in tech_companies:
        print(f"  - {company.name}")
    
    # Search by name containing specific text
    corp_companies = Company.objects.filter(name__icontains='Corp')
    print(f"\nCompanies with 'Corp' in name: {corp_companies.count()}")
    for company in corp_companies:
        print(f"  - {company.name}")
    
    # Get companies ordered by name
    ordered_companies = Company.objects.all().order_by('name')
    print(f"\nAll companies ordered by name:")
    for company in ordered_companies:
        print(f"  - {company.name}")
    
    # Get first company
    first_company = Company.objects.first()
    if first_company:
        print(f"\nFirst company: {first_company.name}")
    
    # Count companies by sector
    sectors = Company.objects.values_list('economic_sector', flat=True).distinct()
    print(f"\nCompanies by sector:")
    for sector in sectors:
        count = Company.objects.filter(economic_sector=sector).count()
        print(f"  - {sector}: {count}")

def demonstrate_crud_operations():
    """Demonstrate Create, Read, Update, Delete operations"""
    print("\n=== CRUD Operations Demo ===\n")
    
    # CREATE
    print("1. CREATE - Creating a new company:")
    new_company = Company.objects.create(
        name='Demo Company Ltd',
        description='A demo company for testing purposes',
        country_of_origin='Australia',
        economic_sector='Demo'
    )
    print(f"✓ Created company: {new_company.name} (ID: {new_company.id})")
    
    # READ
    print(f"\n2. READ - Retrieving company by ID {new_company.id}:")
    retrieved_company = Company.objects.get(id=new_company.id)
    print(f"✓ Retrieved: {retrieved_company.name}")
    
    # UPDATE
    print(f"\n3. UPDATE - Updating company description:")
    retrieved_company.description = "Updated description for demo company"
    retrieved_company.save()
    print(f"✓ Updated description for: {retrieved_company.name}")
    
    # Verify update
    updated_company = Company.objects.get(id=new_company.id)
    print(f"New description: {updated_company.description}")
    
    # DELETE
    print(f"\n4. DELETE - Removing demo company:")
    deleted_name = updated_company.name
    updated_company.delete()
    print(f"✓ Deleted company: {deleted_name}")
    
    # Verify deletion
    try:
        Company.objects.get(id=new_company.id)
        print("✗ Company still exists!")
    except Company.DoesNotExist:
        print("✓ Company successfully deleted")

def main():
    print("=== Django ORM Company Management Demo ===\n")
    
    # Create sample companies
    create_sample_companies()
    
    # Retrieve and display all companies
    companies = retrieve_and_display_companies()
    
    # Demonstrate filtering
    if companies.exists():
        demonstrate_filtering()
        
        # Demonstrate CRUD operations
        demonstrate_crud_operations()
    
    print("\n=== Demo completed successfully! ===")
    print("\nYou can now:")
    print("- View companies in Django admin at: http://127.0.0.1:8000/admin/")
    print("- Access the API at: http://127.0.0.1:8000/api/companies/")
    print("- Use the Django shell: python manage.py shell")

if __name__ == "__main__":
    main()
