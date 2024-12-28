from django.db import models
from django.urls import reverse
from typing import ClassVar

from library.Param import Param


class MyModel(models.Model):

    class Meta:
        abstract = True  # Ensures this class is not created as a database table

    # Subclasses can define these as needed
    NAME_SPACE = ""
    FK_PARAM = Param(None, None)

    @classmethod
    def LOCAL_LIST_URL_NAME(cls) -> str:
        return f"{cls.__name__}_list_url_name"

    @classmethod
    def LOCAL_CREATE_URL_NAME(cls):
        return f"{cls.__name__}_create_url_name"

    @classmethod
    def LOCAL_UPDATE_URL_NAME(cls):
        return f"{cls.__name__}_update_url_name"

    @classmethod
    def LOCAL_DELETE_URL_NAME(cls):
        return f"{cls.__name__}_delete_url_name"

    @classmethod
    def LOCAL_DETAILS_URL_NAME(cls):
        return f"{cls.__name__}_details_url_name"

    @classmethod
    @property
    def LIST_URL_NAME(cls):
        return f"{cls.NAME_SPACE}:{cls.LOCAL_LIST_URL_NAME()}"


    @classmethod
    @property
    def CREATE_URL_NAME(cls):
        return f"{cls.NAME_SPACE}:{cls.LOCAL_CREATE_URL_NAME()}"

    @classmethod
    @property
    def DELETE_URL_NAME(cls):
        return f"{cls.NAME_SPACE}:{cls.LOCAL_DELETE_URL_NAME()}"

    @classmethod
    @property
    def DETAILS_URL_NAME(cls):
        return f"{cls.NAME_SPACE}:{cls.LOCAL_DETAILS_URL_NAME()}"

    @classmethod
    @property
    def UPDATE_URL_NAME(cls):
        return f"{cls.NAME_SPACE}:{cls.LOCAL_UPDATE_URL_NAME()}"

    def get_absolute_url(self):
        """Returns the absolute URL, dynamically handling ForeignKey if provided."""

        if self.FK_PARAM:
            if self.FK_DETAILS_URL_NAME():
                # Use ForeignKey-specific URL if key is provided
                return reverse(self.FK_DETAILS_URL_NAME(),
                               kwargs={self.FK_PARAM.key: getattr(self, self.FK_PARAM.field_name).pk, 'pk': self.pk})

            raise NotImplementedError(f"{self.FK_DETAILS_URL_NAME()} must be defined in the subclass.")

        if self.DETAILS_URL_NAME():
            # Use global URL otherwise
            return reverse(self.DETAILS_URL_NAME(), kwargs={'pk': self.pk})

        raise NotImplementedError(f"{self.DETAILS_URL_NAME()} must be defined in the subclass.")
    #
    # def do_update(self, **kwargs):
    #     """Returns the update URL, dynamically handling ForeignKey if provided."""
    #     # fk_value = kwargs.get(self.FK, None) if self.FK else None
    #
    #     # if self.FK_PARAM and self.FK_UPDATE_URL_NAME:
    #     #     return reverse(self.FK_UPDATE_URL_NAME,
    #     #                    kwargs={self.FK_KEY: getattr(self, self.FK_FIELD_NAME), 'pk': self.pk})
    #     # print('do_update kwargs:', kwargs)
    #
    #     if self.UPDATE_URL_NAME:
    #         return reverse(self.UPDATE_URL_NAME, kwargs={'pk': self.pk})
    #     raise NotImplementedError("UPDATE_URL_NAME or FK_UPDATE_URL_NAME must be defined in the subclass.")
    #
    # def do_delete(self, **kwargs):
    #     """Returns the delete URL, dynamically handling ForeignKey if provided."""
    #     # fk_value = kwargs.get(self.FK, None) if self.FK else None
    #     # print('do_delete kwargs:', kwargs)
    #
    #     # if self.FK_PARAM and self.FK_DELETE_URL_NAME:
    #     #     return reverse(self.FK_DELETE_URL_NAME,
    #     #                    kwargs={self.FK_KEY: getattr(self, self.FK_FIELD_NAME), 'pk': self.pk})
    #
    #     if self.DELETE_URL_NAME:
    #         return reverse(self.DELETE_URL_NAME, kwargs={'pk': self.pk})
    #     raise NotImplementedError("DELETE_URL_NAME or FK_DELETE_URL_NAME must be defined in the subclass.")
