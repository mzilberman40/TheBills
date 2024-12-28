from django.contrib import admin
from handbooks.models import *

tables = [LegalForm, Country, Currency, ResourceGroup, ResourceType, ]

for table in tables:
    admin.site.register(table)