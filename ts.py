# File: view_data.py
# Location: <your_project_folder>

import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'banking_system.settings')
django.setup()

from bank.models import User, Account

# Fetch all users
users = User.objects.all()
print("Users:")
for user in users:
    print(f"Username: {user.username}, Email: {user.email}, Date Joined: {user.date_joined}")

# Fetch all accounts
accounts = Account.objects.all()
print("\nAccounts:")
for account in accounts:
    print(f"User: {account.user.username}, Balance: {account.balance}")

# You can add more queries as needed, such as fetching specific users or accounts
