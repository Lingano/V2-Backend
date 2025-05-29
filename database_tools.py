#!/usr/bin/env python
"""
Database management tools for accessing PostgreSQL via browser
"""

import os
import sys
import subprocess
import webbrowser
from pathlib import Path


def setup_adminer():
    """Download and setup Adminer - lightweight database management tool"""
    import urllib.request

    adminer_path = Path("adminer.php")

    if not adminer_path.exists():
        print("📥 Downloading Adminer...")
        url = "https://github.com/vrana/adminer/releases/download/v4.8.1/adminer-4.8.1.php"
        urllib.request.urlretrieve(url, "adminer.php")
        print("✅ Adminer downloaded successfully!")

    print("\n🌐 Starting PHP server for Adminer...")
    print("📋 Database Connection Info:")
    print("   Server: localhost")
    print("   Username: postgres")
    print("   Password: (leave empty if using trust auth)")
    print("   Database: lingano_db")
    print("\n🔗 Opening browser at: http://localhost:8080")

    # Start PHP server
    subprocess.Popen(["php", "-S", "localhost:8080", "adminer.php"])

    # Open browser
    webbrowser.open("http://localhost:8080")


def setup_web_based_client():
    """Setup a simple web-based PostgreSQL client using Python"""
    print("🔧 Setting up web-based PostgreSQL client...")

    # This would install a Python-based web client
    subprocess.run([sys.executable, "-m", "pip", "install", "flask", "psycopg2-binary"])

    print("✅ Dependencies installed!")


def show_connection_info():
    """Show PostgreSQL connection information"""
    print("\n📊 PostgreSQL Connection Information")
    print("=" * 50)
    print("🏠 Host: localhost")
    print("🔌 Port: 5432")
    print("👤 Username: postgres")
    print("🔑 Password: (check your .env file)")
    print("💾 Database: lingano_db")
    print("=" * 50)

    print("\n🌐 Browser-based Options:")
    print("1. Adminer (Lightweight)")
    print("2. pgAdmin 4 (Full-featured)")
    print("3. Custom Django database viewer")


if __name__ == "__main__":
    show_connection_info()

    choice = input("\nSelect option (1-3): ").strip()

    if choice == "1":
        setup_adminer()
    elif choice == "2":
        print("Install pgAdmin 4 from: https://www.pgadmin.org/download/")
    elif choice == "3":
        print("Creating custom Django database viewer...")
    else:
        print("Invalid choice!")
