#!/usr/bin/env python
"""
PostgreSQL Setup Script for Django
This script helps you set up PostgreSQL for your Django application.
"""

import os
import sys
import subprocess
from pathlib import Path

def print_step(step, message):
    print(f"\n{'='*50}")
    print(f"STEP {step}: {message}")
    print(f"{'='*50}")

def main():
    print("Django PostgreSQL Setup Helper")
    print("This script will help you configure PostgreSQL for your Django app.")
    
    # Step 1: Check if PostgreSQL is installed
    print_step(1, "Checking PostgreSQL Installation")
    try:
        result = subprocess.run(['psql', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ PostgreSQL is installed: {result.stdout.strip()}")
        else:
            print("❌ PostgreSQL is not installed or not in PATH")
            print("Please install PostgreSQL from: https://www.postgresql.org/download/windows/")
            return
    except FileNotFoundError:
        print("❌ PostgreSQL is not installed or not in PATH")
        print("Please install PostgreSQL from: https://www.postgresql.org/download/windows/")
        return
    
    # Step 2: Environment Variables
    print_step(2, "Environment Variables Setup")
    env_vars = {
        'DB_NAME': 'lingano_db',
        'DB_USER': 'postgres',
        'DB_PASSWORD': 'your_password_here',
        'DB_HOST': 'localhost',
        'DB_PORT': '5432'
    }
    
    print("Required environment variables for PostgreSQL:")
    for key, default in env_vars.items():
        current = os.environ.get(key, 'Not set')
        print(f"  {key}: {current} (default: {default})")
    
    print("\nTo set environment variables, you can:")
    print("1. Create a .env file in your project root")
    print("2. Set them in your system environment")
    print("3. Set them temporarily in your terminal session")
    
    # Step 3: Database Creation Instructions
    print_step(3, "Database Creation")
    db_name = os.environ.get('DB_NAME', 'lingano_db')
    db_user = os.environ.get('DB_USER', 'postgres')
    
    print(f"To create the database '{db_name}', run these commands in psql:")
    print(f"1. Connect to PostgreSQL: psql -U {db_user}")
    print(f"2. Create database: CREATE DATABASE {db_name};")
    print(f"3. Grant privileges: GRANT ALL PRIVILEGES ON DATABASE {db_name} TO {db_user};")
    print("4. Exit psql: \\q")
    
    # Step 4: Django Migrations
    print_step(4, "Django Migrations")
    print("After setting up the database, run these Django commands:")
    print("1. python manage.py makemigrations")
    print("2. python manage.py migrate")
    print("3. python manage.py createsuperuser (optional)")
    
    # Step 5: Test Connection
    print_step(5, "Test Database Connection")
    print("To test the connection, run:")
    print("python manage.py dbshell")
    
    print("\n" + "="*50)
    print("Setup completed! Follow the steps above to configure PostgreSQL.")
    print("="*50)

if __name__ == '__main__':
    main()
