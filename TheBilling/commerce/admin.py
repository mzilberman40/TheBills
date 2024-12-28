from django.contrib import admin
from .models import *

tables = [Resource, Project, Contract, Service, ServicePriceHistory]

for table in tables:
    admin.site.register(table)