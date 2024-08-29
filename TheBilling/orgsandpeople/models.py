from django.db import models
from django.db.models import Q

from django.urls import reverse
from django_extensions.db.models import ActivatorModel, TimeStampedModel
from django_extensions.db.fields import AutoSlugField
from pytils.translit import slugify as ru_slugify

from library.my_model import MyModel
from handbooks.models import Country, Currency, ResourceGroup

from django.contrib.auth import get_user_model

User = get_user_model()


class Bank(MyModel, models.Model):
    bik = models.SlugField(unique=True, max_length=9, null=True, blank=True)
    corr_account = models.CharField(max_length=20, unique=False, blank=True, null=True)
    name = models.CharField(max_length=256, blank=False)
    short_name = models.CharField(max_length=128, blank=False, unique=True)
    slug = AutoSlugField(populate_from=['short_name'], unique=True,
                         db_index=True, slugify_function=ru_slugify)
    country = models.ForeignKey(Country, null=True, blank=True, on_delete=models.SET_NULL)
    # address = models.CharField(max_length=256, blank=True)
    swift = models.SlugField(max_length=32, blank=True, null=True, unique=True)
    # status = models.CharField(max_length=16,blank=True)
    # registration_date = models.DateField(blank=True, null=True)
    # liquidation_date = models.DateField(blank=True, null=True)
    notes = models.TextField(max_length=512, blank=True)
    user = models.ForeignKey(User, verbose_name='User', on_delete=models.CASCADE, default=1)

    details_url = 'orgsandpeople:bank_details_url'
    update_url = 'orgsandpeople:bank_update_url'
    delete_url = 'orgsandpeople:bank_delete_url'

    class Meta:
        verbose_name = "Bank"
        verbose_name_plural = "Banks"

    # def __repr__(self):
    #     return f"{self.short_name}: BIK: {self.bik}, SWIFT: {self.swift}"

    def __str__(self):
        return f"{self.short_name}"


class BusinessUnit(MyModel, TimeStampedModel, ActivatorModel, models.Model):
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
    user = models.ForeignKey(User, verbose_name='Owner', on_delete=models.CASCADE, default=1)

    details_url = 'orgsandpeople:bu_details_url'
    update_url = 'orgsandpeople:bu_update_url'
    delete_url = 'orgsandpeople:bu_delete_url'

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

    @property
    def e_mails(self):
        return ', '.join([f"{email.email}:{email.email_type}"
                          if email.email_type else email.email
                          for email in self.emails.all()])


class Email(models.Model):
    email = models.EmailField(unique=True)
    bu = models.ForeignKey('BusinessUnit', on_delete=models.CASCADE, related_name='emails')
    email_type = models.CharField(max_length=10, null=True, blank=True)

    class Meta:
        verbose_name = "Email"
        verbose_name_plural = "Emails"

    def __str__(self):
        return f"{self.email} ({self.email_type})" if self.email_type else self.email


class Address(MyModel, models.Model):
    country = models.ForeignKey(Country, on_delete=models.PROTECT)
    address_data = models.JSONField(blank=True, null=True)
    owner = models.ForeignKey('BusinessUnit', on_delete=models.PROTECT)

    class Meta:
        verbose_name = "Address"
        verbose_name_plural = "Addresses"

    def __str__(self):
        return f"{self.country} {self.address_data}"


class Account(ActivatorModel, models.Model):
    name = models.CharField(max_length=32)
    business_unit = models.ForeignKey('orgsandpeople.BusinessUnit',
                                      on_delete=models.CASCADE,
                                      related_name='accounts')
    bank = models.ForeignKey('orgsandpeople.Bank', on_delete=models.CASCADE)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=20)
    starting_balance = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.CharField(max_length=512, blank=True)

    details_url = 'orgsandpeople:bu_account_detail_url'
    update_url = 'orgsandpeople:bu_account_update_url'
    delete_url = 'orgsandpeople:bu_account_delete_url'

    def __str__(self):
        # return (f"{self.name}: {self.account_number} - {self.bank.name} - {self.currency.code}"
        #         f" - {'Active' if self.status else 'Inactive'}")
        return self.name

    def get_absolute_url(self, *args, **kwargs):
        if self.details_url:
            return reverse(self.details_url, kwargs={'bu_pk': self.business_unit.pk, 'pk': self.pk })
        raise NotImplementedError

    def do_delete(self, *args, **kwargs):
        if self.delete_url:
            return reverse(self.delete_url, kwargs={'pk': self.pk, 'bu_pk': self.business_unit.pk})
        raise NotImplementedError

    def do_update(self, *args, **kwargs):
        # print("Update", kwargs)
        if self.update_url:
            print(self.update_url)

            return reverse(self.update_url, kwargs={'pk': self.pk, 'bu_pk': self.business_unit.pk})
        raise NotImplementedError

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['bank', 'account_number'],
                name='unique_bank_account_number'
            )
        ]
        verbose_name = "Account"
        verbose_name_plural = "Accounts"
