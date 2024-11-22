from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django_extensions.db.models import TitleSlugDescriptionModel, TimeStampedModel, ActivatorModel

from handbooks.models import ResourceType
from library.my_model import MyModel
from orgsandpeople.models import BusinessUnit


User = get_user_model()


class Resource(MyModel, TimeStampedModel, ActivatorModel, models.Model):
    name = models.CharField(max_length=120, unique=True)
    rtype = models.ForeignKey(ResourceType, on_delete=models.CASCADE, related_name='resources')
    description = models.TextField(max_length=512, null=True, blank=True)
    available = models.BooleanField(default=True)
    owner = models.ForeignKey(BusinessUnit, on_delete=models.CASCADE, related_name='resources')
    user = models.ForeignKey(User, verbose_name='user', on_delete=models.CASCADE)

    details_url = 'commerce:resource_details_url'
    update_url = 'commerce:resource_update_url'
    delete_url = 'commerce:resource_delete_url'

    class Meta:
        verbose_name = "Resource"
        verbose_name_plural = "Resources"
        ordering = ('name',)

    def __str__(self):
        return f"{self.name}, {self.rtype}, {self.owner}"


class Project(MyModel, models.Model):
    title = models.CharField(max_length=120, unique=True)
    description = models.TextField(max_length=512, null=True, blank=True)
    beneficiary = models.ForeignKey(BusinessUnit, on_delete=models.CASCADE, related_name='projects')

    details_url = 'commerce:project_details_url'
    update_url = 'commerce:project_update_url'
    delete_url = 'commerce:project_delete_url'

    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"
        ordering = ('title',)

    def __str__(self):
        return f"{self.title}, {self.beneficiary}"


class Agreement(MyModel, TimeStampedModel, ActivatorModel, models.Model):
    STATUS_CHOICES = [
        ('planned', 'Planned'),
        ('active', 'Active'),
        ('paused', 'Paused'),
        ('finished', 'Finished'),
    ]

    number = models.CharField(max_length=32, unique=True)
    title = models.CharField(max_length=120)
    description = models.TextField(max_length=512, null=True, blank=True)
    seller = models.ForeignKey(BusinessUnit, on_delete=models.CASCADE, related_name='sellers')
    buyer = models.ForeignKey(BusinessUnit, on_delete=models.CASCADE, related_name='buyers')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='projects')
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='planned',
    )

    details_url = 'commerce:agreement_details_url'
    update_url = 'commerce:agreement_update_url'
    delete_url = 'commerce:agreement_delete_url'

    class Meta:
        verbose_name = "Agreement"
        verbose_name_plural = "Agreements"
        ordering = ('number', 'title',)

    def __str__(self):
        return f"{self.number} ({self.get_status_display()})"

    def clean(self):
        """Ensure Seller and Buyer are different and validate dates."""
        if self.seller == self.buyer:
            raise ValidationError("Seller and Buyer must be different.")
        if self.end_date and self.start_date and self.end_date < self.start_date:
            raise ValidationError("End date must be after start date.")