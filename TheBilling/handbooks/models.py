from django.db import models
# from django.urls import reverse
from django_extensions.db.models import ActivatorModel, TimeStampedModel
# from pytils.translit import slugify as ru_slugify
# from django_extensions.db.fields import AutoSlugField
from django.contrib.auth import get_user_model
from library.my_model import MyModel

User = get_user_model()

class LegalForm(MyModel):
    short_name = models.SlugField(max_length=32, unique=True, allow_unicode=True)
    full_name = models.CharField(max_length=256, unique=True)
    description = models.CharField(max_length=1024, blank=True)

    NAME_SPACE = 'handbooks'

    class Meta:
        app_label = 'handbooks'
        verbose_name = "LegalForm"
        verbose_name_plural = "LegalForms"
        ordering = ('short_name',)

    def __str__(self):
        return self.short_name


class Country(MyModel):
    """
    Format dadata:
    value	Значение одной строкой (как показывается в списке подсказок)
    data.code	Цифровой код страны  ISO 3166
    data.alfa2	Буквенный код альфа-2
    data.alfa3	Буквенный код альфа-3
    data.name_short	Краткое наименование страны
    data.name	Полное официальное наименование страны

    """
    iso3166 = models.PositiveSmallIntegerField(primary_key=True)
    alfa2 = models.SlugField(max_length=2, unique=True)
    alfa3 = models.SlugField(max_length=3, unique=True)
    eng_name = models.CharField(max_length=512, unique=True)
    eng_name_official = models.CharField(max_length=512, blank=True, null=True)
    rus_name_short = models.CharField(max_length=64, unique=True)  # data.name_short
    rus_name = models.CharField(max_length=128, unique=True)     # data.name
    rus_name_official = models.CharField(max_length=512, unique=True)    # value

    NAME_SPACE = 'handbooks'

    class Meta:
        app_label = 'handbooks'
        verbose_name = "Country"
        verbose_name_plural = "Countries"
        ordering = ('eng_name',)

    def __str__(self):
        return f"{self.eng_name}"


class Currency(MyModel):
    numeric = models.PositiveSmallIntegerField(primary_key=True)
    name = models.CharField(max_length=64, unique=True)
    code = models.CharField(max_length=5, unique=True)

    NAME_SPACE = 'handbooks'

    class Meta:
        app_label = 'handbooks'
        verbose_name = "Currency"
        verbose_name_plural = "Currencies"
        ordering = ('name',)

    def __str__(self):
        return f"{self.name}"


class ResourceGroup(MyModel):
    name = models.CharField(max_length=120, unique=True)
    description = models.CharField(max_length=1024, blank=True)

    NAME_SPACE = 'handbooks'

    class Meta:
        app_label = 'handbooks'
        verbose_name = "Resource Group"
        verbose_name_plural = "Resource Groups"
        ordering = ('name',)

    def __str__(self):
        return f"{self.name}"

class ResourceType(MyModel):
    rtype = models.CharField(max_length=120, unique=True, verbose_name="ResourceType")
    group = models.ForeignKey(ResourceGroup, on_delete=models.RESTRICT, related_name='rtypes')
    description = models.TextField(max_length=1024, blank=True)

    NAME_SPACE = 'handbooks'

    class Meta:
        app_label = 'handbooks'
        verbose_name = "ResourceType"
        verbose_name_plural = "ResourceTypes"
        ordering = ('rtype',)

    def __str__(self):
        return f"{self.rtype}"

class ServiceName(MyModel):
    name = models.CharField(max_length=120, unique=True)
    description = models.CharField(max_length=1024, blank=True)

    NAME_SPACE = 'handbooks'

    class Meta:
        app_label = 'handbooks'
        verbose_name = "Service Name"
        verbose_name_plural = "Service Names"
        ordering = ('name',)

    def __str__(self):
        return f"{self.name}"
