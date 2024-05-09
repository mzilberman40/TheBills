import uuid

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from pytils.translit import slugify as ru_slugify
from django_extensions.db.fields import AutoSlugField
from django_extensions.db.models import TitleSlugDescriptionModel, TimeStampedModel, ActivatorModel


class LegalForm(models.Model):
    short_name = models.SlugField(max_length=32, unique=True, allow_unicode=True)
    full_name = models.CharField(max_length=256, unique=True)
    description = models.CharField(max_length=1024, blank=True)
    slug = AutoSlugField(populate_from=['short_name'], unique=True, db_index=True, slugify_function=ru_slugify)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, verbose_name='Owner', on_delete=models.CASCADE, default=1)

    class Meta:
        verbose_name = "LegalForm"
        verbose_name_plural = "LegalForms"

    def __str__(self):
        return f"{self.short_name}"

    def get_absolute_url(self):
        return reverse('handbooks:legal_form_details_url', kwargs={'pk': self.pk})

    def do_update(self):
        return reverse('handbooks:legal_form_update_url', kwargs={'pk': self.pk})

    def do_delete(self):
        return reverse('handbooks:legal_form_delete_url', kwargs={'pk': self.pk})


class Country(models.Model):
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
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, verbose_name='Owner', on_delete=models.CASCADE, default=1)

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"

    def __str__(self):
        return f"{self.eng_name}"

    def get_absolute_url(self):
        return reverse('handbooks:country_details_url', kwargs={'pk': self.pk})

    def do_update(self):
        return reverse('handbooks:country_update_url', kwargs={'pk': self.pk})

    def do_delete(self):
        return reverse('handbooks:country_delete_url', kwargs={'pk': self.pk})

#
# class Bank(ActivatorModel, TimeStampedModel, models.Model):
#     bik = models.SlugField(unique=True, max_length=9, null=True, blank=True)
#     corr_account = models.CharField(max_length=20, unique=False, blank=True, null=True)
#     name = models.CharField(max_length=256, blank=False)
#     short_name = models.CharField(max_length=128, blank=False, unique=True)
#     slug = AutoSlugField(populate_from=['short_name'], unique=True, db_index=True, slugify_function=ru_slugify)
#     address = models.CharField(max_length=256, blank=True)
#     swift = models.SlugField(max_length=32, blank=True, null=True, unique=True)
#     status = models.CharField(max_length=16,blank=True)
#     registration_date = models.DateField(blank=True, null=True)
#     liquidation_date = models.DateField(blank=True, null=True)
#     notes = models.TextField(max_length=512, blank=True)
#
#     class Meta:
#         verbose_name = "Bank"
#         verbose_name_plural = "Banks"
#
#     def __repr__(self):
#         return f"{self.short_name}: BIK: {self.bik}, SWIFT: {self.swift}"
#
#     def __str__(self):
#         return f"{self.short_name}"
#
#     def get_absolute_url(self):
#         return reverse('bank_details_url', kwargs={'pk': self.pk})
#
#     def do_update(self):
#         return reverse('bank_update_url', kwargs={'pk': self.pk})
#
#     def do_delete(self):
#         return reverse('bank_delete_url', kwargs={'pk': self.pk})
