from django.urls import reverse
from abc import ABC, abstractmethod
from django.db import models


class MyModel(models.Model):
    details_url_name = None
    update_url_name = None
    delete_url_name = None

    class Meta:
        abstract = True

    def get_absolute_url_name(self):
        if self.details_url_name:
            return reverse(self.details_url_name, kwargs={'pk': self.pk})
        raise NotImplementedError("details_url_name must be defined in the subclass")

    def do_update(self):
        if self.update_url_name:
            return reverse(self.update_url_name, kwargs={'pk': self.pk})
        raise NotImplementedError("update_url_name must be defined in the subclass")

    def do_delete(self):
        # print("Deleting....")
        if self.delete_url_name:
            # print(self.delete_url_name, self.pk)
            return reverse(self.delete_url_name, kwargs={'pk': self.pk})
        raise NotImplementedError("delete_url_name must be defined in the subclass")
