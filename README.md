# V2-Backend for Lingano

This repository contains the Django backend for the Lingano application. It provides API endpoints, handles database interactions, and includes web scraping functionalities.

## Overview

The V2-Backend is built with Django and Django REST Framework, using PostgreSQL as the database. It's designed to serve as the core of the Lingano application, managing data and business logic.

## Getting Started

These instructions will guide you through setting up the project on your local machine for development and testing.

### Prerequisites

Before you begin, ensure you have the following installed:

-   Python (version specified in `runtime.txt`, if available, otherwise latest stable)
-   Pip (Python package installer)
-   PostgreSQL (See [POSTGRESQL_SETUP.md](POSTGRESQL_SETUP.md) for setup instructions)
-   Git

### Installation

1.  **Clone the repository:**

    ```bash
    git clone <repository-url>
    cd V2-Backend
    ```

2.  **Create a virtual environment (recommended):**

    ```bash
    python -m venv venv
    # On Windows
    .\venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up the database:**

    -   Follow the instructions in [POSTGRESQL_SETUP.md](POSTGRESQL_SETUP.md) to install and configure PostgreSQL.
    -   Ensure your database `lingano_db` is created and the user `postgres` has access.
    -   If you plan to use pgAdmin, refer to [PGADMIN_SETUP.md](PGADMIN_SETUP.md).

5.  **Create a `.env` file:**
    Based on the `POSTGRESQL_SETUP.md`, your `.env` file at the root of the project should look like this if you are using trust authentication:

    ```env
    DEBUG=True
    SECRET_KEY=your_secret_django_key_here # Replace with a strong secret key
    DATABASE_URL=postgres://postgres@localhost:5432/lingano_db
    # For trust authentication, no password is required.
    # If you set a password for the 'postgres' user for 'lingano_db', add it:
    # DATABASE_URL=postgres://postgres:your_password@localhost:5432/lingano_db
    ```

    **Important:** Generate a new `SECRET_KEY`. You can use an online Django secret key generator or run `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'` in your shell.

6.  **Apply database migrations:**

    ```bash
    python manage.py migrate
    ```

7.  **Create a superuser (for accessing the Django admin panel):**
    ```bash
    python manage.py createsuperuser
    ```
    Follow the prompts to set up your admin username and password.

## Running the Application

### Development Server

To run the Django development server:

```bash
python manage.py runserver
```

The application will typically be available at `http://127.0.0.1:8000/`.

### Using Gunicorn (for production-like environments)

The `Procfile` specifies how to run the application using Gunicorn:

```bash
gunicorn --pythonpath backend core.wsgi
```

(Note: The `Procfile` has `backend` in the pythonpath. Ensure your project structure matches this or adjust the command/`Procfile` accordingly. Typically, it might just be `gunicorn core.wsgi` if `manage.py` is at the root.)

## Key Features

-   **RESTful APIs:** Provides various API endpoints for the Lingano application.
-   **Database Management:** Uses PostgreSQL for robust data storage.
-   **Web Scraping:** Includes modules for scraping company data.
-   **User Authentication:** Manages user accounts and authentication (details in `authentication/` and potentially `django-allauth` if fully configured).
-   **Market Simulation:** Contains logic for market simulation (see `market/` app).

## API Endpoints

The application exposes several API endpoints. Some of the initial endpoints include (refer to `POSTGRESQL_SETUP.md` and your URL configurations for a complete list):

-   **Admin Interface**: `http://127.0.0.1:8000/admin/`
-   **API Hello**: `http://127.0.0.1:8000/api/hello/`
-   **API Current Time**: `http://127.0.0.1:8000/api/current-time/`
-   **Health Check**: `http://127.0.0.1:8000/health/`
-   **Test Page**: `http://127.0.0.1:8000/test/`
-   **Debug Info**: `http://127.0.0.1:8000/debug/`

Explore `api/urls.py`, `market/urls.py`, and `core/urls.py` for more detailed API routes.

## Project Structure

A brief overview of the project directory structure:

```
V2-Backend/
├── api/                # Main application for API logic, scraping
├── authentication/     # User authentication logic
├── core/               # Core Django project settings, ASGI/WSGI configs
├── market/             # Market simulation application
├── staticfiles/        # Collected static files
├── manage.py           # Django's command-line utility
├── requirements.txt    # Project dependencies
├── Procfile            # Heroku deployment configuration
├── README.md           # This file
├── POSTGRESQL_SETUP.md # PostgreSQL setup guide
├── PGADMIN_SETUP.md    # pgAdmin setup guide
└── .env                # Environment variables (create this locally)
```

## Management Commands

The project includes custom management commands:

-   `api/management/commands/`:
    -   `company_demo.py`
    -   `fetch_companies.py`
    -   `scheduled_scraper.py`
-   `market/management/commands/`:
    -   `simulate_market.py`

Run them using `python manage.py <command_name>`.

## Contributing

Details on how to contribute to the project will be added here. (Placeholder)

## License

This project's license information will be added here. (Placeholder)
