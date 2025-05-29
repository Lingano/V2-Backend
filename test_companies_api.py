"""
Test script to demonstrate creating and retrieving Company models via API
Run this script while the Django server is running on http://127.0.0.1:8000/
"""

import requests
import json

# API endpoints
BASE_URL = "http://127.0.0.1:8000/api"
COMPANIES_URL = f"{BASE_URL}/companies/"

def create_company(company_data):
    """Create a new company via API"""
    try:
        response = requests.post(
            COMPANIES_URL,
            data=company_data,
            headers={'Content-Type': 'application/json'} if isinstance(company_data, str) else None
        )
        if response.status_code == 201:
            print(f"✓ Created company: {response.json()['name']}")
            return response.json()
        else:
            print(f"✗ Failed to create company: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"✗ Error creating company: {e}")
        return None

def get_all_companies():
    """Retrieve all companies via API"""
    try:
        response = requests.get(COMPANIES_URL)
        if response.status_code == 200:
            companies = response.json()
            print(f"✓ Retrieved {len(companies)} companies")
            return companies
        else:
            print(f"✗ Failed to retrieve companies: {response.status_code} - {response.text}")
            return []
    except requests.exceptions.RequestException as e:
        print(f"✗ Error retrieving companies: {e}")
        return []

def get_company_by_id(company_id):
    """Retrieve a specific company by ID via API"""
    try:
        response = requests.get(f"{COMPANIES_URL}{company_id}/")
        if response.status_code == 200:
            company = response.json()
            print(f"✓ Retrieved company: {company['name']}")
            return company
        else:
            print(f"✗ Failed to retrieve company {company_id}: {response.status_code} - {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"✗ Error retrieving company {company_id}: {e}")
        return None

def main():
    print("=== Company API Test Script ===\n")
    
    # Sample company data
    sample_companies = [
        {
            "name": "TechCorp Solutions",
            "description": "A leading technology company specializing in software development and cloud services.",
            "country_of_origin": "United States",
            "economic_sector": "Technology"
        },
        {
            "name": "Green Energy Ltd",
            "description": "Renewable energy company focused on solar and wind power solutions.",
            "country_of_origin": "Germany",
            "economic_sector": "Energy"
        },
        {
            "name": "Global Finance Corp",
            "description": "International financial services and investment banking.",
            "country_of_origin": "United Kingdom",
            "economic_sector": "Finance"
        }
    ]
    
    print("1. Creating sample companies...")
    created_companies = []
    for company_data in sample_companies:
        result = create_company(company_data)
        if result:
            created_companies.append(result)
    
    print(f"\nCreated {len(created_companies)} companies successfully.\n")
    
    print("2. Retrieving all companies...")
    all_companies = get_all_companies()
    
    if all_companies:
        print("\n=== All Companies ===")
        for company in all_companies:
            print(f"""
ID: {company['id']}
Name: {company['name']}
Description: {company['description']}
Country: {company['country_of_origin']}
Sector: {company['economic_sector']}
{'-' * 50}""")
    
    print(f"\nTotal companies in database: {len(all_companies)}\n")
    
    # Test retrieving a specific company
    if all_companies:
        print("3. Testing retrieval of specific company...")
        first_company = all_companies[0]
        retrieved_company = get_company_by_id(first_company['id'])
        
        if retrieved_company:
            print(f"Successfully retrieved: {retrieved_company['name']}")
    
    print("\n=== Test completed! ===")
    print("You can now:")
    print("- View companies in Django admin at: http://127.0.0.1:8000/admin/")
    print("- Access the API at: http://127.0.0.1:8000/api/companies/")
    print("- Test individual company endpoints at: http://127.0.0.1:8000/api/companies/1/")

if __name__ == "__main__":
    main()
