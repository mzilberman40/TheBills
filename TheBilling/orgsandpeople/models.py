from django.core.exceptions import ValidationError
from django.core.validators import validate_email, RegexValidator
from django.db import models
from django.db.models import Q

# from django.urls import reverse
from django_extensions.db.models import ActivatorModel, TimeStampedModel
from django_extensions.db.fields import AutoSlugField
from pytils.translit import slugify as ru_slugify

# from library.Param import Param
from library.my_model import MyModel
from handbooks.models import Country, Currency, ResourceGroup

from django.contrib.auth import get_user_model
# from library.mydecorators import tracer


User = get_user_model()
DEBUG = 0

class Bank(MyModel):
    bik = models.SlugField(unique=True, max_length=9, null=True, blank=True)
    corr_account = models.CharField(max_length=20, unique=False, blank=True, null=True)
    name = models.CharField(max_length=256, blank=False)
    short_name = models.CharField(max_length=128, blank=False, unique=True)
    slug = AutoSlugField(populate_from=['short_name'], unique=True,
                         db_index=True, slugify_function=ru_slugify)
    country = models.ForeignKey(Country, null=True, blank=True, on_delete=models.SET_NULL)
    swift = models.SlugField(max_length=32, blank=True, null=True, unique=True)
    notes = models.TextField(max_length=1024, blank=True)
    user = models.ForeignKey(User, verbose_name='User', on_delete=models.PROTECT)

    NAME_SPACE = 'orgsandpeople'

    class Meta:
        verbose_name = "Bank"
        verbose_name_plural = "Banks"

    # def __repr__(self):
    #     return f"{self.short_name}: BIK: {self.bik}, SWIFT: {self.swift}"

    def __str__(self):
        return f"{self.short_name}"


class BusinessUnit(TimeStampedModel, ActivatorModel, MyModel):
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
    payment_name = models.CharField(max_length=128, unique=True)
    slug = AutoSlugField(populate_from=['short_name'], unique=True,
                         db_index=True, slugify_function=ru_slugify)
    legal_form = models.ForeignKey('handbooks.LegalForm', on_delete=models.PROTECT, verbose_name='Legal Form')
    country = models.ForeignKey('handbooks.Country', on_delete=models.PROTECT, verbose_name='Country')
    address = models.CharField(max_length=512, blank=True, null=True)
    notes = models.TextField(max_length=8192, blank=True)
    user = models.ForeignKey(User, verbose_name='Owner', on_delete=models.PROTECT)

    NAME_SPACE = 'orgsandpeople'

    class Meta:
        verbose_name = "BusinessUnit"
        verbose_name_plural = "BusinessUnits"
        app_label = 'orgsandpeople'

        constraints = [
            models.CheckConstraint(
                check=Q(inn__isnull=False) | Q(payment_name__isnull=False),
                name='inn_or_payment_name_required'
            )
        ]

    def __str__(self):
        return f"{self.payment_name}"

    @property
    def e_mails(self):
        """
        To use field 'e_mails' to display all emails in detailView for example
        """
        return ','.join(str(e) for e in Email.objects.filter(bu=self))


class Email(ActivatorModel, MyModel):
    email = models.EmailField(unique=True)
    bu = models.ForeignKey('BusinessUnit', on_delete=models.CASCADE, related_name='emails')
    email_type = models.SlugField(max_length=64, null=True, blank=True)
    verified = models.BooleanField(
        default=False,
        verbose_name="Verified",
        help_text="Indicates if the email has been verified."
    )

    NAME_SPACE = 'orgsandpeople'

    class Meta:
        verbose_name = "Email"
        verbose_name_plural = "Emails"
        app_label = 'orgsandpeople'

    def __str__(self):
        return f"{self.email} ({self.email_type})" if self.email_type else self.email

    def clean(self):
        # Call the parent class's clean method to ensure any inherited validation is maintained
        super().clean()

        # Validate email format
        try:
            validate_email(self.email)
        except ValidationError:
            raise ValidationError({'email': f"'{self.email}' is not a valid email address."})

        # Ensure email is unique to avoid duplications (handled in the model level)
        if Email.objects.filter(email=self.email).exclude(pk=self.pk).exists():
            raise ValidationError(
                {'email': f"The email address '{self.email}' is already in use by another BusinessUnit."})

    def save(self, *args, **kwargs):
        self.full_clean()  # Enforce model-level validation before saving
        super(Email, self).save(*args, **kwargs)


# class TelegramData(models.Model):
#     """
#     Model to store Telegram data for a user.
#     """
#     bu = models.ForeignKey(BusinessUnit, on_delete=models.PROTECT, related_name='telegram_data')
#     tg_id = models.BigIntegerField(primary_key=True, unique=True, verbose_name="Telegram ID",
#         help_text="Unique Telegram User ID."
#     )
#     tg_type = models.SlugField(max_length=32, null=True, blank=True)
#     tg_username = models.CharField(max_length=32, null=True, blank=True,
#         validators=[
#             RegexValidator(
#                 regex=r'^[a-zA-Z0-9_]{5,32}$',
#                 message="Telegram username must be 5-32 characters long and contain only letters, numbers, and underscores."
#             )
#         ],
#         verbose_name="Telegram Username",
#         help_text="Username of the user in Telegram."
#     )
#     is_bot = models.BooleanField(
#         default=False,
#         verbose_name="Is Bot",
#         help_text="Indicates whether the Telegram account is a bot."
#     )
#     created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
#     updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")
#
#     NAME_SPACE = 'orgsandpeople'
#
#     # DETAILS_URL_NAME = 'orgsandpeople:bu_telegram_url_name'
#     # UPDATE_URL_NAME = 'orgsandpeople:bu_telegram_update_url_name'
#     # DELETE_URL_NAME = 'orgsandpeople:bu_telegram_delete_url_name'
#     # LIST_URL_NAME = 'orgsandpeople:bu_telegrams_url_name'
#
#     class Meta:
#        app_label = 'orgsandpeople'
#         verbose_name = "Telegram Data"
#         verbose_name_plural = "Telegram Data"
#         ordering = ['-created_at']
#
#     def __str__(self):
#         return f"{self.bu.short_name}'s Telegram Data"

class PhoneNumber(ActivatorModel, MyModel):
    """
    Model to store Phone numbers for a user.
    """
    bu = models.ForeignKey(BusinessUnit, on_delete=models.PROTECT, related_name='phone_numbers')
    phone_number = models.CharField(
        max_length=15, unique=True, verbose_name="Phone Number",
        help_text="Unique Phone Number.",
        validators=[
            RegexValidator(
                regex=r'^\+?[1-9]\d{1,14}$',
                message="Enter a valid international phone number starting with '+' or country code."
            )
        ],

    )
    phone_type = models.SlugField(max_length=32, null=True, blank=True)
    is_for_call = models.BooleanField(default=True, verbose_name="Is For-Call")
    is_for_SMS = models.BooleanField(default=False, verbose_name="Is For-SMS")
    is_for_whatsapp = models.BooleanField(default=False, verbose_name="Is For-WhatsApp")
    is_for_telegram = models.BooleanField(default=False, verbose_name="Is For-Telegram")

    verified = models.BooleanField(
        default=False,
        verbose_name="Verified",
        help_text="Indicates if the phone number has been verified."
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    NAME_SPACE = 'orgsandpeople'

    # DETAILS_URL_NAME = 'orgsandpeople:bu_phone_detail_url_name'
    # UPDATE_URL_NAME = 'orgsandpeople:bu_phone_update_url_name'
    # DELETE_URL_NAME = 'orgsandpeople:bu_phone_delete_url_name'
    # LIST_URL_NAME = 'orgsandpeople:bu_phones_url_name'

    class Meta:
        app_label = 'orgsandpeople'
        verbose_name = "Phone Number"
        verbose_name_plural = "Phone Numbers"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.phone_number} (Primary: {self.phone_type})"

class Account(ActivatorModel, MyModel):
    name = models.CharField(max_length=32)
    business_unit = models.ForeignKey('orgsandpeople.BusinessUnit',
                                      on_delete=models.CASCADE,
                                      related_name='accounts')
    bank = models.ForeignKey('orgsandpeople.Bank', on_delete=models.CASCADE)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=128)
    starting_balance = models.DecimalField(max_digits=10, decimal_places=2)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.CharField(max_length=512, blank=True)

    NAME_SPACE = 'orgsandpeople'

    # DETAILS_URL_NAME = 'orgsandpeople:bu_account_detail_url_name'
    # UPDATE_URL_NAME = 'orgsandpeople:bu_account_update_url_name'
    # DELETE_URL_NAME = 'orgsandpeople:bu_account_delete_url_name'
    # LIST_URL_NAME = 'orgsandpeople:bu_accounts_url_name'

    def __str__(self):
        return self.name

    # def get_absolute_url_name(self, *args, **kwargs):
    #     if self.details_url_name:
    #         return reverse(self.details_url_name, kwargs={'bu_pk': self.business_unit.pk, 'pk': self.pk })
    #     raise NotImplementedError
    #
    # def do_delete(self, *args, **kwargs):
    #     if self.delete_url_name:
    #         return reverse(self.delete_url_name, kwargs={'pk': self.pk, 'bu_pk': self.business_unit.pk})
    #     raise NotImplementedError
    #
    # def do_update(self, *args, **kwargs):
    #     # print("Update", kwargs)
    #     if self.update_url_name:
    #         # print(self.update_url_name)
    #         return reverse(self.update_url_name, kwargs={'pk': self.pk, 'bu_pk': self.business_unit.pk})
    #     raise NotImplementedError

    class Meta:
        app_label = 'orgsandpeople'
        constraints = [
            models.UniqueConstraint(
                fields=['bank', 'account_number'],
                name='unique_bank_account_number'
            )
        ]
        verbose_name = "Account"
        verbose_name_plural = "Accounts"
