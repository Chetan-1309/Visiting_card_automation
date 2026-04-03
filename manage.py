#!/usr/bin/env python
"""
manage.py — Django's command-line tool.
You'll use this to run your server, create database tables, etc.

Common commands:
  python manage.py runserver        → Start the development server
  python manage.py makemigrations   → Detect model changes
  python manage.py migrate          → Apply changes to the database
  python manage.py createsuperuser  → Create an admin account
"""

import os
import sys

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'visitingcard.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError("Couldn't import Django. Did you run: pip install django?") from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
