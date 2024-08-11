from django.db import models
from djmoney.models.fields import MoneyField
from django.db.models import Q
from django.urls import reverse
from django.contrib.auth.models import User
from pytils.translit import slugify as ru_slugify
from django_extensions.db.fields import AutoSlugField
from django_extensions.db.models import TitleSlugDescriptionModel, TimeStampedModel, ActivatorModel

from handbooks.models import ResourceGroup
from orgsandpeople.models import BusinessUnit


class Resource(TimeStampedModel, ActivatorModel, models.Model):
    name = models.CharField(max_length=120)
    owner = models.ForeignKey(BusinessUnit, on_delete=models.CASCADE, related_name='resources')
    group = models.ForeignKey(ResourceGroup, on_delete=models.CASCADE, related_name='resources')
    description = models.TextField()
    available = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Resource"
        verbose_name_plural = "Resources"
        ordering = ('name',)

    def __str__(self):
        return f"{self.name}, {self.owner}"