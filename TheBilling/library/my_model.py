from django.urls import reverse
from abc import ABC, abstractmethod


class MyModel:
    details_url = None
    update_url = None
    delete_url = None

    class Meta:
        abstract = True

    def get_absolute_url(self):
        if self.details_url:
            return reverse(self.details_url, kwargs={'pk': self.pk})
        raise NotImplementedError

    def do_update(self):
        if self.update_url:
            return reverse(self.update_url, kwargs={'pk': self.pk})
        raise NotImplementedError

    def do_delete(self):
        if self.delete_url:
            return reverse(self.delete_url, kwargs={'pk': self.pk})
        raise NotImplementedError
