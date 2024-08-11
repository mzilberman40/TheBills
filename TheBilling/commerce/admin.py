from django.contrib import admin
from .models import *

tables = []

for table in tables:
    admin.site.register(table)