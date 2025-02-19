from django.contrib import admin
from .models import *

tables = [Resource, Project, Contract, Service, ServicePrice]

for table in tables:
    admin.site.register(table)