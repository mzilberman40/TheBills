import moneyed
from django.db import models
from djmoney.models.fields import MoneyField
from django.db.models import Q
from django.urls import reverse
from django.contrib.auth.models import User
from pytils.translit import slugify as ru_slugify
from django_extensions.db.fields import AutoSlugField
from django_extensions.db.models import TitleSlugDescriptionModel, TimeStampedModel, ActivatorModel



