from django.db import models
from django.db.models import Q

from django.urls import reverse
from django.contrib.auth.models import User
from django_extensions.db.models import ActivatorModel, TimeStampedModel
from pytils.translit import slugify as ru_slugify
from django_extensions.db.fields import AutoSlugField
import moneyed
from pytils.translit import slugify as ru_slugify

import config
from handbooks.models import Country


def get_currencies():
    currencies = [moneyed.CURRENCIES.get(c) for c in config.CURRENCIES]
    return {c.code: c.name for c in currencies}


class Bank(TimeStampedModel, models.Model):
    bik = models.SlugField(unique=True, max_length=9, null=True, blank=True)
    corr_account = models.CharField(max_length=20, unique=False, blank=True, null=True)
    name = models.CharField(max_length=256, blank=False)
    short_name = models.CharField(max_length=128, blank=False, unique=True)
    slug = AutoSlugField(populate_from=['short_name'], unique=True, db_index=True, slugify_function=ru_slugify)
    country = models.ForeignKey(Country, null=True, blank=True, on_delete=models.SET_NULL)
    # address = models.CharField(max_length=256, blank=True)
    swift = models.SlugField(max_length=32, blank=True, null=True, unique=True)
    # status = models.CharField(max_length=16,blank=True)
    # registration_date = models.DateField(blank=True, null=True)
    # liquidation_date = models.DateField(blank=True, null=True)
    notes = models.TextField(max_length=512, blank=True)
    user = models.ForeignKey(User, verbose_name='User', on_delete=models.CASCADE, default=1)

    class Meta:
        verbose_name = "Bank"
        verbose_name_plural = "Banks"

    # def __repr__(self):
    #     return f"{self.short_name}: BIK: {self.bik}, SWIFT: {self.swift}"

    def __str__(self):
        return f"{self.short_name}"

    def get_absolute_url(self):
        return reverse('orgsandpeople:bank_details_url', kwargs={'pk': self.pk})

    def do_update(self):
        return reverse('orgsandpeople:bank_update_url', kwargs={'pk': self.pk})

    def do_delete(self):
        return reverse('orgsandpeople:bank_delete_url', kwargs={'pk': self.pk})


class BusinessUnit(TimeStampedModel, ActivatorModel, models.Model):
    """
    inn - is a pk of this model.
    But not all BU have inn.
    For Russia:
        - for person: 12 digits
        - for organization: 10 digits
    For all which inn unknown or doesn't exist:
        15 digits starting with 999.
    """
    inn = models.SlugField(max_length=15, unique=True, null=True, blank=True, verbose_name='INN')
    ogrn = models.SlugField(max_length=20, null=True, blank=True, unique=True)
    first_name = models.CharField(max_length=32, blank=True)
    middle_name = models.CharField(max_length=32, blank=True)
    last_name = models.CharField(max_length=32, blank=True)
    full_name = models.CharField(
        max_length=256,
        help_text="For organization input it's name hear without legal-form. "
                  "For person it can be filled automatically")
    short_name = models.CharField(max_length=128, unique=True)
    # is in an intimate relationship ))
    special_status = models.BooleanField(default=False, verbose_name="Special Status")
    # payment_name is unique name for BU. Not necessary if INN exists
    payment_name = models.CharField(max_length=128, unique=True, null=True, blank=True)
    slug = AutoSlugField(populate_from=['short_name'], unique=True,
                         db_index=True, slugify_function=ru_slugify)
    legal_form = models.ForeignKey('handbooks.LegalForm', on_delete=models.PROTECT,
                                   verbose_name='Legal Form')
    country = models.ForeignKey('handbooks.Country', on_delete=models.PROTECT,
                                verbose_name='Country')
    notes = models.CharField(max_length=512, blank=True)
    owner = models.ForeignKey(User, verbose_name='Owner', on_delete=models.CASCADE, default=1)

    class Meta:
        verbose_name = "BusinessUnit"
        verbose_name_plural = "BusinessUnits"

        constraints = [
            models.CheckConstraint(
                check=Q(inn__isnull=False) | Q(payment_name__isnull=False),
                name='not_both_null'
            )
        ]

    def __str__(self):
        return f"{self.payment_name}"

    def get_absolute_url(self):
        return reverse('orgsandpeople:bu_details_url', kwargs={'pk': self.pk})

    def do_update(self):
        return reverse('orgsandpeople:bu_update_url', kwargs={'pk': self.pk})

    def do_delete(self):
        return reverse('orgsandpeople:bu_delete_url', kwargs={'pk': self.pk})


class Email(TimeStampedModel, models.Model):
    email = models.EmailField(unique=True)
    owner = models.ForeignKey('BusinessUnit', on_delete=models.PROTECT, related_name='emails')

    class Meta:
        verbose_name = "Email"
        verbose_name_plural = "Emails"

    def __str__(self):
        return f"{self.email}"

    def get_absolute_url(self):
        return reverse('emails_list_url', kwargs={'pk': self.pk})

    def do_update(self):
        return reverse('email_update_url', kwargs={'pk': self.pk})

    def do_delete(self):
        return reverse('email_delete_url', kwargs={'pk': self.pk})


class Address(TimeStampedModel, models.Model):
    country = models.ForeignKey(Country, on_delete=models.PROTECT)
    address_data = models.JSONField(blank=True, null=True)
    owner = models.ForeignKey('BusinessUnit', on_delete=models.PROTECT)

    class Meta:
        verbose_name = "Address"
        verbose_name_plural = "Addresses"

    def __str__(self):
        return f"{self.country} {self.address_data}"

    def get_absolute_url(self):
        return reverse('address_list_url', kwargs={'pk': self.pk})

    def do_update(self):
        return reverse('address_update_url', kwargs={'pk': self.pk})

    def do_delete(self):
        return reverse('address_delete_url', kwargs={'pk': self.pk})


class Account(TimeStampedModel, ActivatorModel, models.Model):
    business_unit = models.ForeignKey('orgsandpeople.BusinessUnit', on_delete=models.PROTECT)
    bank = models.ForeignKey('orgsandpeople.Bank', on_delete=models.PROTECT)
    number = models.SlugField(max_length=64)
    currency = models.CharField(max_length=3, choices=get_currencies)
    starting_balance = models.FloatField(default=0)
    starting_date = models.DateField(blank=True)
    notes = models.CharField(max_length=512, blank=True)

    class Meta:
        verbose_name = "Account"
        verbose_name_plural = "Accounts"
        unique_together = ['bank', 'number']

    def __str__(self):
        return f"{self.business_unit}: rs{self.number} in {self.bank}, currency: {self.currency}"

    def get_absolute_url(self):
        return reverse('account_details_url', kwargs={'pk': self.pk})

    def do_update(self):
        return reverse('account_update_url', kwargs={'pk': self.pk})

    def do_delete(self):
        return reverse('account_delete_url', kwargs={'pk': self.pk})
