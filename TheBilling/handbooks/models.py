from django.db import models
from django.urls import reverse


class LegalForm(models.Model):
    short_name = models.SlugField(max_length=32, unique=True, allow_unicode=True)
    full_name = models.CharField(max_length=256, unique=True)
    description = models.CharField(max_length=1024, blank=True)

    class Meta:
        verbose_name = "LegalForm"
        verbose_name_plural = "LegalForms"

    def __str__(self):
        return f"{self.short_name}"

    def get_absolute_url(self):
        return reverse('legal_form_details_url', kwargs={'pk': self.pk})

    def do_update(self):
        return reverse('legal_form_update_url', kwargs={'pk': self.pk})

    def do_delete(self):
        return reverse('legal_form_delete_url', kwargs={'pk': self.pk})

