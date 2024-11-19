from django.contrib.auth import get_user_model
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