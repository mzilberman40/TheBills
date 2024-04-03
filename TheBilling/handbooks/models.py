from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from pytils.translit import slugify as pt_slugify
from django_extensions.db.fields import AutoSlugField
from django_extensions.db.models import TitleSlugDescriptionModel, TimeStampedModel


class LegalForm(models.Model):
    short_name = models.SlugField(max_length=32, unique=True, allow_unicode=True)
    full_name = models.CharField(max_length=256, unique=True)
    description = models.CharField(max_length=1024, blank=True)
    slug = AutoSlugField(populate_from=['short_name'], unique=True, db_index=True, slugify_function=pt_slugify)
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
