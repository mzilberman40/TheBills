from django.contrib import admin
from orgsandpeople.models import *

tables = [Bank, BusinessUnit, Email, TelegramData, PhoneNumber, Account]

for table in tables:
    admin.site.register(table)
