# Company Model API Documentation

## Overview

This Django project now includes a complete Company model with API endpoints for creating and retrieving company data. The setup includes:

1. **Company Model** - Django model for storing company information
2. **REST API** - API endpoints for CRUD operations
3. **Django Admin** - Admin interface for managing companies
4. **Database Integration** - SQLite database with proper migrations

## Company Model Structure

The `Company` model includes the following fields:

-   `name` (CharField, max 255 characters) - Company name
-   `description` (TextField) - Company description
-   `country_of_origin` (CharField, max 100 characters) - Country where company originated
-   `economic_sector` (CharField, max 100 characters) - Economic sector (e.g., Technology, Finance)

## API Endpoints

### Base URL: `http://127.0.0.1:8000/api/`

### 1. List all companies / Create new company

-   **URL:** `/companies/`
-   **Methods:**
    -   `GET` - Retrieve all companies
    -   `POST` - Create a new company

#### GET Example:

```bash
curl http://127.0.0.1:8000/api/companies/
```

#### POST Example:

```bash
curl -X POST http://127.0.0.1:8000/api/companies/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "TechCorp Solutions",
    "description": "A leading technology company",
    "country_of_origin": "United States",
    "economic_sector": "Technology"
  }'
```

### 2. Retrieve/Update/Delete specific company

-   **URL:** `/companies/<id>/`
-   **Methods:**
    -   `GET` - Retrieve specific company
    -   `PUT` - Update entire company
    -   `PATCH` - Partial update
    -   `DELETE` - Delete company

#### GET Example:

```bash
curl http://127.0.0.1:8000/api/companies/1/
```

## Using Django ORM (Python Code)

### Creating Companies

```python
from api.models import Company

# Create a single company
company = Company.objects.create(
    name="TechCorp Solutions",
    description="A leading technology company",
    country_of_origin="United States",
    economic_sector="Technology"
)

# Bulk create companies
companies_data = [
    {"name": "Company A", "description": "...", "country_of_origin": "USA", "economic_sector": "Tech"},
    {"name": "Company B", "description": "...", "country_of_origin": "UK", "economic_sector": "Finance"},
]
companies = [Company(**data) for data in companies_data]
Company.objects.bulk_create(companies)
```

### Retrieving Companies

```python
# Get all companies
all_companies = Company.objects.all()

# Get specific company by ID
company = Company.objects.get(id=1)

# Filter companies
us_companies = Company.objects.filter(country_of_origin="United States")
tech_companies = Company.objects.filter(economic_sector="Technology")

# Search by name
companies_with_corp = Company.objects.filter(name__icontains="Corp")

# Get first/last company
first_company = Company.objects.first()
last_company = Company.objects.last()

# Count companies
total_count = Company.objects.count()
us_count = Company.objects.filter(country_of_origin="United States").count()
```

### Advanced Queries

```python
# Order companies
companies_by_name = Company.objects.all().order_by('name')
companies_by_country = Company.objects.all().order_by('country_of_origin', 'name')

# Get distinct values
sectors = Company.objects.values_list('economic_sector', flat=True).distinct()
countries = Company.objects.values_list('country_of_origin', flat=True).distinct()

# Complex filtering
companies = Company.objects.filter(
    economic_sector__in=['Technology', 'Finance'],
    country_of_origin='United States'
).order_by('name')
```

### Updating Companies

```python
# Update single company
company = Company.objects.get(id=1)
company.description = "Updated description"
company.save()

# Bulk update
Company.objects.filter(country_of_origin="USA").update(country_of_origin="United States")
```

### Deleting Companies

```python
# Delete single company
company = Company.objects.get(id=1)
company.delete()

# Delete multiple companies
Company.objects.filter(economic_sector="Demo").delete()
```

## Django Admin Interface

Access the admin interface at: `http://127.0.0.1:8000/admin/`

The Company model is registered with the following features:

-   List view shows: name, country_of_origin, economic_sector
-   Filtering by: country_of_origin, economic_sector
-   Search by: name, description
-   Ordering by: name

## Database Migrations

The database table has been created with the migration:

```bash
python manage.py makemigrations api
python manage.py migrate
```

## Starting the Server

To run the development server:

```bash
cd "C:\Users\m41hm\Desktop\LinganoCorp\LiganoRoot\V2-Backend"
python manage.py runserver
```

The server will be available at: `http://127.0.0.1:8000/`

## Testing the API

You can test the API using:

1. **Browser** - Visit `http://127.0.0.1:8000/api/companies/` to see the browsable API
2. **curl** - Use command line HTTP requests
3. **Python requests** - Use the requests library for programmatic access
4. **Django shell** - Use `python manage.py shell` for direct ORM access

## File Structure

```
api/
├── models.py          # Company model definition
├── serializers.py     # DRF serializers for API
├── views.py           # API views (ListCreateAPIView, RetrieveUpdateDestroyAPIView)
├── urls.py            # URL routing for API endpoints
├── admin.py           # Django admin configuration
└── migrations/
    └── 0001_initial.py # Database migration for Company model
```

## Next Steps

You can now:

1. Create companies via the API or Django admin
2. Retrieve companies using various filtering options
3. Update and delete companies as needed
4. Integrate this API with frontend applications
5. Add authentication and permissions as required
6. Extend the model with additional fields if needed
