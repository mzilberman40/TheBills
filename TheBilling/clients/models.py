from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q
from django.urls import reverse
from django_extensions.db import models as emodels
from django_extensions.db.fields.json import JSONField


class BusinessUnit(emodels.ActivatorModel, emodels.TimeStampedModel, models.Model):
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
                                 help_text="For organization input it's name without legal-form."
                                           "For person it can be filled automatically")
    short_name = models.CharField(max_length=128, unique=True)
    # payment_name is unique name for BU. Not necessary if INN exists
    payment_name = models.CharField(max_length=128, unique=True, null=True, blank=True)
    legal_form = models.ForeignKey('handbooks.LegalForm', on_delete=models.PROTECT, null=True, blank=True)
    address = models.TextField(max_length=256, blank=True)
    address_data = models.JSONField(blank=True, null=True)
    date_updated = models.DateTimeField(blank=True, auto_now=True)
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
        return f"{self.short_name}"

    def get_absolute_url(self):
        return reverse('business_unit_details_url', kwargs={'pk': self.pk})

    def do_update(self):
        return reverse('business_unit_update_url', kwargs={'pk': self.pk})

    def do_delete(self):
        return reverse('business_unit_delete_url', kwargs={'pk': self.pk})
