from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django_extensions.db.models import TitleSlugDescriptionModel, TimeStampedModel, ActivatorModel

from django.utils.timezone import now  # For handling start_time

from handbooks.models import ResourceType, Currency, ServiceName
from library.my_model import MyModel
from orgsandpeople.models import BusinessUnit

User = get_user_model()


class Project(MyModel):
    title = models.CharField(max_length=120, unique=True)
    description = models.TextField(max_length=512, null=True, blank=True)
    beneficiary = models.ForeignKey(BusinessUnit, on_delete=models.PROTECT, related_name='projects')

    class Meta:
        app_label = 'commerce'
        verbose_name = "Project"
        verbose_name_plural = "Projects"
        ordering = ('title',)

    def __str__(self):
        return f"{self.title}"

    NAME_SPACE = 'commerce'


class Resource(TimeStampedModel, MyModel):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('reserved', 'Reserved'),
        ('rented', 'Rented'),
        ('testing', 'Testing'),
        ('sold', 'Sold'),
    ]

    name = models.CharField(max_length=120, unique=True)
    rtype = models.ForeignKey(ResourceType, on_delete=models.PROTECT, related_name='resources')
    description = models.TextField(max_length=512, null=True, blank=True)
    current_status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='available',
        verbose_name="Current Status"
    )
    business_unit = models.ForeignKey(BusinessUnit, on_delete=models.PROTECT, related_name='resources')
    project = models.ForeignKey(Project, on_delete=models.PROTECT, related_name='resources')
    user = models.ForeignKey(User, verbose_name='user', on_delete=models.PROTECT)

    class Meta:
        app_label = 'commerce'
        verbose_name = "Resource"
        verbose_name_plural = "Resources"
        ordering = ('name',)

    def __str__(self):
        return self.name


class Contract(TimeStampedModel, MyModel):
    STATUS_CHOICES = [
        ('planned', 'Planned'),
        ('active', 'Active'),
        ('paused', 'Paused'),
        ('finished', 'Finished'),
    ]
    NAME_SPACE = 'commerce'

    number = models.CharField(max_length=32, unique=True)
    title = models.CharField(max_length=120)
    description = models.TextField(max_length=512, null=True, blank=True)
    seller = models.ForeignKey(BusinessUnit, on_delete=models.PROTECT, related_name='scontracts')
    buyer = models.ForeignKey(BusinessUnit, on_delete=models.PROTECT, related_name='bcontracts')
    project = models.ForeignKey(Project, on_delete=models.PROTECT, related_name='projects')
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='planned',
    )
    user = models.ForeignKey(User, verbose_name='User', on_delete=models.PROTECT)

    class Meta:
        app_label = 'commerce'
        verbose_name = "Contract"
        verbose_name_plural = "Contracts"
        ordering = ('number', 'title',)

    def __str__(self):
        return f"{self.number}"

    def clean(self):
        """Ensure Seller and Buyer are different and validate dates."""
        if self.seller == self.buyer:
            raise ValidationError("Seller and Buyer must be different.")
        if self.end_date and self.start_date and self.end_date < self.start_date:
            raise ValidationError("End date must be after start date.")


class ServicePriceHistory(models.Model):
    service = models.ForeignKey(
        'Service',
        on_delete=models.CASCADE,
        related_name='price_history',
        verbose_name="Service"
    )
    new_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="New Price")
    effective_date = models.DateField(verbose_name="Effective Date")
    changed_at = models.DateTimeField(default=now, verbose_name="Changed At")
    changed_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name="Changed By"
    )

    class Meta:
        verbose_name = "Service Price History"
        verbose_name_plural = "Service Price Histories"
        ordering = ['-effective_date', '-changed_at']
        app_label = 'commerce'

    def __str__(self):
        return f"Price change for {self.service.service_name}: {self.new_price} effective {self.effective_date}"

    NAME_SPACE = 'commerce'


class Service(MyModel):
    SERVICE_TYPE_CHOICES = [
        ('one_time', 'One-time'),
        ('recurring', 'Recurring'),
    ]

    BILLING_FREQUENCY_CHOICES = [
        ('daily', 'Daily'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    ]

    STATUS_CHOICES = [
        ('planned', 'Planned'),
        ('active', 'Active'),
        ('paused', 'Paused'),
        ('finished', 'Finished'),
    ]
    # service_name = models.CharField(max_length=255, verbose_name="Service Name")

    service_name = models.ForeignKey(ServiceName,
        on_delete=models.PROTECT,
        verbose_name="Service Name",
        related_name="services"
    )
    service_type = models.CharField(max_length=50, choices=SERVICE_TYPE_CHOICES, verbose_name="Service Type")
    billing_frequency = models.CharField(
        max_length=50,
        choices=BILLING_FREQUENCY_CHOICES,
        null=True,
        blank=True,
        verbose_name="Billing Frequency (Recurring only)"
    )
    start_date = models.DateField(null=True, blank=True, verbose_name="Start Date")
    finish_date = models.DateField(null=True, blank=True, verbose_name="Finish Date")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price")
    currency = models.ForeignKey(
        Currency,
        on_delete=models.PROTECT,
        verbose_name="Currency",
        related_name="services"
    )
    contract = models.ForeignKey(
        'Contract',
        on_delete=models.PROTECT,
        verbose_name="Contract",
        related_name="services"
    )
    resource = models.OneToOneField(
        'Resource',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="Linked Resource",
        related_name="services",
        limit_choices_to={'current_status': 'available'}
    )
    description = models.TextField(null=True, blank=True, verbose_name="Description")
    user = models.ForeignKey(User, verbose_name='Owner', on_delete=models.PROTECT)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
    )

    def clean(self):
        """
        Validation logic:
        - Ensure billing frequency is required for recurring services.
        - Validate start_time and finish_time for both service types.
        - Ensure only 'available' resources can be linked to the service.
        """
        super().clean()

        if self.start_date and self.finish_date and self.start_date >= self.finish_date:
            raise ValidationError("Start date must be earlier than finish date.")

        if self.service_type == 'recurring':
            if not self.billing_frequency:
                raise ValidationError("Billing frequency is required for recurring services.")
        elif self.service_type == 'one_time':
            if self.billing_frequency:
                raise ValidationError("Billing frequency is not applicable for one-time services.")

        if self.resource:
            if self.resource.current_status not in ['available']:
                raise ValidationError(
                    f"The resource '{self.resource.name}' cannot be bound because its current status is '{self.resource.get_current_status_display()}'."
                )

    def save(self, *args, **kwargs):
        """
        Update the resource's status when the service is created or updated.
        """
        if self.pk is None and self.resource:  # New service
            if self.resource.current_status != 'available':
                raise ValidationError(f"The resource '{self.resource.name}' is not available for binding.")
            self.resource.current_status = 'reserved'
            self.resource.save()
        super().save(*args, **kwargs)

    def start_service(self):
        """
        Start the service, update start_time, and change resource status to 'rented'.
        """
        if not self.resource:
            raise ValidationError("No resource is linked to this service.")
        if self.resource.current_status != 'reserved':
            raise ValidationError(f"The resource '{self.resource.name}' must be reserved before starting the service.")
        self.start_date = now()  # Record the current time
        self.resource.current_status = 'rented'
        self.resource.save()
        self.save()

    def update_price(self, new_price, effective_date, user=None):
        """
        Update the price of the service and record the change in the price history.
        The effective date determines when the new price becomes active.
        """
        # Create a history record
        ServicePriceHistory.objects.create(
            service=self,
            new_price=new_price,
            effective_date=effective_date,
            changed_by=user
        )
        # Update the current price only if the effective date is today or earlier
        if effective_date <= now().date():
            self.price = new_price
            self.save()

    def __str__(self):
        return self.service_name

    class Meta:
        verbose_name = "Service"
        verbose_name_plural = "Services"
        ordering = ('service_name',)
        app_label = 'commerce'

    NAME_SPACE = 'commerce'
