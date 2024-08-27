from django.contrib.auth import get_user_model
from django.db import models
from django_extensions.db.models import TitleSlugDescriptionModel, TimeStampedModel, ActivatorModel

from handbooks.models import ResourceGroup
from library.my_model import MyModel
from orgsandpeople.models import BusinessUnit


User = get_user_model()


# class Resource(MyModel, TimeStampedModel, ActivatorModel, models.Model):
#     name = models.CharField(max_length=120, unique=True)
#     group = models.ForeignKey(ResourceGroup, on_delete=models.CASCADE, related_name='resources')
#     description = models.TextField()
#     available = models.BooleanField(default=True)
#     user = models.ForeignKey(User, verbose_name='Owner', on_delete=models.CASCADE, default=1)
#
#     details_url = 'commerce:resource_details_url'
#     update_url = 'commerce:resource_update_url'
#     delete_url = 'commerce:resource_delete_url'
#
#     class Meta:
#         verbose_name = "Resource"
#         verbose_name_plural = "Resources"
#         ordering = ('name',)
#
#     def __str__(self):
#         return f"{self.name}, {self.user}"