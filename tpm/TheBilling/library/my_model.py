from django.urls import reverse
from abc import ABC, abstractmethod
from django.db import models


class MyModel(models.Model):
    details_url = None
    update_url = None
    delete_url = None

    class Meta:
        abstract = True

    def get_absolute_url(self):
        if self.details_url:
            return reverse(self.details_url, kwargs={'pk': self.pk})
        raise NotImplementedError("details_url must be defined in the subclass")

    def do_update(self):
        if self.update_url:
            return reverse(self.update_url, kwargs={'pk': self.pk})
        raise NotImplementedError("update_url must be defined in the subclass")

    def do_delete(self):
        # print("Deleting....")
        if self.delete_url:
            # print(self.delete_url, self.pk)
            return reverse(self.delete_url, kwargs={'pk': self.pk})
        raise NotImplementedError("delete_url must be defined in the subclass")
