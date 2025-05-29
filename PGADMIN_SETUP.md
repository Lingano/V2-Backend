# 🐘 pgAdmin 4 Setup Guide

## 📥 Installation Steps

### 1. Download pgAdmin 4

-   Go to: https://www.pgadmin.org/download/pgadmin-4-windows/
-   Download the Windows installer (latest version)
-   Run the installer as Administrator

### 2. Launch pgAdmin 4

-   After installation, launch pgAdmin 4
-   It will open in your default web browser
-   Create a master password when prompted

## 🔌 Database Connection Configuration

### Connection Details for Your Django Project:

```
General Tab:
  Name: Lingano Django DB

Connection Tab:
  Host name/address: localhost
  Port: 5432
  Maintenance database: postgres
  Username: postgres
  Password: [see your .env file or leave empty if using trust auth]

Advanced Tab:
  DB restriction: lingano_db
```

### Step-by-Step Connection:

1. **Right-click "Servers" in pgAdmin**
2. **Select "Create" > "Server..."**
3. **Fill in the details:**

    **General Tab:**

    - Name: `Lingano Django Database`

    **Connection Tab:**

    - Host: `localhost`
    - Port: `5432`
    - Username: `postgres`
    - Password: `[your password from .env file]`
    - Save password: ✅ (optional)

4. **Click "Save"**

## 🔍 What You'll See in pgAdmin

After connecting, you'll see:

### Database Structure:

```
📂 Servers
  └── 📂 Lingano Django Database
      └── 📂 Databases
          └── 📂 lingano_db
              └── 📂 Schemas
                  └── 📂 public
                      └── 📂 Tables
                          ├── 📋 api_company (your scraped companies)
                          ├── 📋 auth_user (Django users)
                          ├── 📋 django_admin_log
                          └── 📋 ... (other Django tables)
```

### Key Tables for Your Project:

-   **`api_company`** - Your scraped company data
-   **`market_company`** - Market simulation companies
-   **`auth_user`** - Django admin users
-   **`django_migrations`** - Migration history

## 🎯 Useful pgAdmin Features

### 1. **Query Tool**

-   Right-click on `lingano_db` > "Query Tool"
-   Run SQL queries directly:

```sql
-- View all companies
SELECT * FROM api_company;

-- Count companies by sector
SELECT economic_sector, COUNT(*)
FROM api_company
GROUP BY economic_sector;

-- Recent companies
SELECT name, country_of_origin, economic_sector
FROM api_company
ORDER BY id DESC
LIMIT 10;
```

### 2. **Data Viewer**

-   Right-click any table > "View/Edit Data" > "All Rows"
-   Browse data with pagination
-   Edit records directly

### 3. **Database Dashboard**

-   Monitor database performance
-   View active connections
-   Check database size

## 🔧 Troubleshooting

### Connection Issues:

1. **Check PostgreSQL is running:**

    ```powershell
    Get-Service postgresql*
    ```

2. **Verify database exists:**

    ```powershell
    psql -U postgres -l
    ```

3. **Test connection from command line:**
    ```powershell
    psql -U postgres -d lingano_db -h localhost -p 5432
    ```

### Authentication Issues:

-   If using trust authentication, leave password empty
-   Check your `.env` file for the correct password
-   Ensure PostgreSQL `pg_hba.conf` allows connections

## 🚀 Quick Access URLs

Once pgAdmin is running:

-   **pgAdmin Web Interface:** http://localhost:5432 (or the port shown during startup)
-   **Django Admin:** http://127.0.0.1:8000/admin/
-   **Django API:** http://127.0.0.1:8000/api/

## 📊 Recommended Queries for Your Project

```sql
-- Company statistics
SELECT
    COUNT(*) as total_companies,
    COUNT(DISTINCT country_of_origin) as unique_countries,
    COUNT(DISTINCT economic_sector) as unique_sectors
FROM api_company;

-- Top countries by company count
SELECT country_of_origin, COUNT(*) as company_count
FROM api_company
GROUP BY country_of_origin
ORDER BY company_count DESC
LIMIT 10;

-- Companies by sector
SELECT economic_sector, COUNT(*) as count
FROM api_company
GROUP BY economic_sector
ORDER BY count DESC;

-- Recent scraper activity
SELECT name, country_of_origin, economic_sector, id
FROM api_company
ORDER BY id DESC
LIMIT 20;
```

Happy database browsing! 🎉
