from django.contrib import admin
from handbooks.models import *

tables = [LegalForm, Country]

for table in tables:
    admin.site.register(table)