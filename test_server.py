#!/usr/bin/env python
"""
Simple test script to check if Django server can start
"""

import os
import sys
import django
from django.core.management import execute_from_command_line

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DealFlowAI.settings')
django.setup()

if __name__ == '__main__':
    print("Testing Django server startup...")
    try:
        # Try to start the server
        execute_from_command_line(['manage.py', 'runserver', '127.0.0.1:8000'])
    except Exception as e:
        print(f"Error starting server: {e}")
        import traceback
        traceback.print_exc() 