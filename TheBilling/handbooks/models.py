from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django_extensions.db.models import ActivatorModel, TimeStampedModel
from pytils.translit import slugify as ru_slugify
from django_extensions.db.fields import AutoSlugField

from library.my_model import MyModel


class LegalForm(MyModel, models.Model):
    short_name = models.SlugField(max_length=32, unique=True, allow_unicode=True)
    full_name = models.CharField(max_length=256, unique=True)
    description = models.CharField(max_length=1024, blank=True)
    # slug = AutoSlugField(populate_from=['short_name'], unique=True, db_index=True, slugify_function=ru_slugify)
    owner = models.ForeignKey(User, verbose_name='Owner', on_delete=models.CASCADE, default=1)

    details_url = 'handbooks:legal_form_details_url'
    update_url = 'handbooks:legal_form_update_url'
    delete_url = 'handbooks:legal_form_delete_url'

    class Meta:
        verbose_name = "LegalForm"
        verbose_name_plural = "LegalForms"
        ordering = ('short_name',)

    def __str__(self):
        return f"{self.short_name}"


class Country(MyModel, models.Model):
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
    eng_name = models.CharField(max_length=64, unique=True)
    eng_name_official = models.CharField(max_length=64, blank=True, null=True)
    rus_name_short = models.CharField(max_length=64, unique=True)  # data.name_short
    rus_name = models.CharField(max_length=64, unique=True)     # data.name
    rus_name_official = models.CharField(max_length=64, unique=True)    # value

    details_url = 'handbooks:country_details_url'
    update_url = 'handbooks:country_update_url'
    delete_url = 'handbooks:country_delete_url'

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"
        ordering = ('eng_name',)

    def __str__(self):
        return f"{self.eng_name}"


class Currency(MyModel, models.Model):
    numeric = models.PositiveSmallIntegerField(primary_key=True)
    name = models.CharField(max_length=64, unique=True)
    code = models.CharField(max_length=3, unique=True)

    details_url = 'handbooks:currency_details_url'
    update_url = 'handbooks:currency_update_url'
    delete_url = 'handbooks:currency_delete_url'

    class Meta:
        verbose_name = "Currency"
        verbose_name_plural = "Currencies"
        ordering = ('name',)

    def __str__(self):
        return f"{self.name}"


class ResourceGroup(models.Model):
    name = models.CharField(max_length=120)
    description = models.CharField(max_length=1024, blank=True)

    details_url = 'handbooks:res_group_details_url'
    update_url = 'handbooks:res_group_update_url'
    delete_url = 'handbooks:res_group_delete_url'

    class Meta:
        verbose_name = "Resource Group"
        verbose_name_plural = "Resource Groups"
        ordering = ('name',)

    def __str__(self):
        return f"{self.name}"


