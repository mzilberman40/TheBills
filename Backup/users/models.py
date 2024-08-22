# from django.contrib.auth.models import User
from django.db import models

from django_extensions.db.models import (
    TimeStampedModel,
    ActivatorModel,
    )

from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)


class UserManager(BaseUserManager):
    """ Manager for users """
    def create_user(self, email, password=None, **extra_fields):
        """
        Create, save and return a new user
        """
        if not email:
            raise ValueError("User must have an email")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create, save and return a new superuser
        :param email:
        :param password:
        :param extra_fields:
        :return:
        """

        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system"""
    email = models.EmailField(max_length=255, unique=True)
    # name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class UserProfile(TimeStampedModel, ActivatorModel, models.Model):
    """
    users.UserProfile
    Stores a single user profile entry related to :model:`auth.User`
    """
    class Meta:
        verbose_name_plural = 'User profiles'
        ordering = ["id"]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    telephone = models.CharField(
        verbose_name="Contact telephone number", max_length=255, null=True, blank=True
    )
    address = models.CharField(verbose_name="Address", max_length=100, null=True, blank=True)
    avatar = models.ImageField(
        default='default_avatar.jpg', upload_to='avatar', null=True, blank=True
    )

    def full_name(self):
        """
        Return full name or email
        """
        return f'{self.user.email}: {self.first_name.capitalize()} {self.last_name.capitalize()}'

    def __str__(self):
        return self.full_name()
