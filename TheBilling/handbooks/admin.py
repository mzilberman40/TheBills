from django.contrib import admin
from .models import *

tables = [LegalForm]

for table in tables:
    admin.site.register(table)