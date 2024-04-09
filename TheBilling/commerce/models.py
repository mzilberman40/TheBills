import moneyed
from django.db import models
from djmoney.models.fields import MoneyField
from django.db.models import Q
from django.urls import reverse
from django.contrib.auth.models import User
from pytils.translit import slugify as ru_slugify
from django_extensions.db.fields import AutoSlugField
from django_extensions.db.models import TitleSlugDescriptionModel, TimeStampedModel, ActivatorModel


class BusinessUnit(TimeStampedModel, models.Model):
    """
    inn - is a pk of this model.
    But not all BU have inn.
    For Russia:
        - for person: 12 digits
        - for organization: 10 digits
    For all which inn unknown or doesn't exist:
        15 digits starting with 999.
    """
    special_status = models.BooleanField(default=False)
    inn = models.SlugField(max_length=15, unique=True, null=True, blank=True)
    ogrn = models.SlugField(max_length=20, null=True, blank=True, unique=True)
    first_name = models.CharField(max_length=32, blank=True)
    middle_name = models.CharField(max_length=32, blank=True)
    last_name = models.CharField(max_length=32, blank=True)
    full_name = models.CharField(max_length=256,
                                 help_text="For organization input it's name hear without legal-form. "
                                           "For person it can be filled automatically")
    short_name = models.CharField(max_length=128, unique=True)

    # payment_name is unique name for BU. Not necessary if INN exists
    payment_name = models.CharField(max_length=128, unique=True, null=True, blank=True)
    legal_form = models.ForeignKey('handbooks.LegalForm', on_delete=models.PROTECT, null=True, blank=True)
    address = models.TextField(max_length=256, blank=True)
    address_data = models.JSONField(blank=True, null=True)
    notes = models.CharField(max_length=512, blank=True)
    slug = AutoSlugField(populate_from=['full_name'], unique=True, db_index=True, slugify_function=ru_slugify)
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
        return f"{self.short_name}"

    def get_absolute_url(self):
        return reverse('business_unit_details_url', kwargs={'pk': self.pk})

    def do_update(self):
        return reverse('business_unit_update_url', kwargs={'pk': self.pk})

    def do_delete(self):
        return reverse('business_unit_delete_url', kwargs={'pk': self.pk})


class Email(models.Model):
    email = models.EmailField(unique=True)
    owner = models.ForeignKey('BusinessUnit', on_delete=models.PROTECT)

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


class Account(ActivatorModel, TimeStampedModel, models.Model):
    business_unit = models.ForeignKey('commerce.BusinessUnit', on_delete=models.PROTECT)
    bank = models.ForeignKey('handbooks.Bank', on_delete=models.PROTECT)
    number = models.SlugField(max_length=32)
    balance = MoneyField(max_digits=14, decimal_places=2, default_currency='USD')
    starting_date = models.DateField(blank=True)
    notes = models.CharField(max_length=512, blank=True)
    owner = models.ForeignKey(User, verbose_name='Owner', on_delete=models.CASCADE, default=1)

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
