from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, pre_init, post_init
# from django.contrib.auth.models import User
from django.dispatch import receiver
from . models import UserProfile

User = get_user_model()


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        obj, created = UserProfile.objects.get_or_create(user=instance)

