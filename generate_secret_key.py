#!/usr/bin/env python
"""
Generate a new Django secret key for production use
Run this script and copy the output to your .env file
"""

import os
import sys
from pathlib import Path

# Add the Django project to the path
sys.path.append(str(Path(__file__).parent))

try:
    from django.core.management.utils import get_random_secret_key

    print("🔑 Generated new Django SECRET_KEY:")
    print("-" * 60)
    print(get_random_secret_key())
    print("-" * 60)
    print("\n📋 Copy this key to your .env file:")
    print(f"SECRET_KEY={get_random_secret_key()}")
    print("\n⚠️  Keep this key secret and never commit it to version control!")

except ImportError:
    print("❌ Django not installed. Please install Django first:")
    print("pip install django")
