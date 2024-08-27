#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from django.core.management.commands.runserver import Command as runserver
import shutil

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'geminiapp.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

try:
    path = os.getcwd() + '/db.sqlite3'

    # print("Copy database")			# debug
    # print(f"Path: {path}")			# debug

    shutil.copyfile(path, '/tmp/db.sqlite3')
except Exception as e:
    print(e)		# print error message

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    runserver.default_addr = "0.0.0.0"
    runserver.default_addr_ipv6 = "::"
    runserver.default_port = port
    main()
