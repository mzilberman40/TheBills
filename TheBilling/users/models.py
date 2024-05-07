from django.contrib.auth.models import User
from django.db import models

# these are model abstracts from django extensions
from django_extensions.db.models import (
    TimeStampedModel,
    ActivatorModel,
    )


class UserProfile(TimeStampedModel, ActivatorModel, models.Model):
    """
    users.UserProfile
    Stores a single user profile entry related to :model:`auth.User`
    """
    class Meta:
        verbose_name_plural = 'User profiles'
        ordering = ["id"]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telephone = models.CharField(verbose_name="Contact telephone number", max_length=255, null=True, blank=True)
    address = models.CharField(verbose_name="Address", max_length=100, null=True, blank=True)
    avatar = models.ImageField(default='default_avatar.jpg', upload_to='avatar', null=True, blank=True)

    def full_name(self):
        """
        Return full name or email
        """
        if self.user.first_name and self.user.last_name:
            return f'{self.user.first_name.capitalize()} {self.user.last_name.capitalize()}'
        if self.user.email:
            return self.user.email
        return self.user.email

    def __str__(self):
        return self.full_name()
