from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver


class UserProfile(models.Model):
    'User Profile'
    user = models.OneToOneField(
        User,
        unique=True,
        verbose_name='user',
        related_name='profile',
    )


@receiver(models.signals.post_save, sender=User)
def get_or_create_user_profile(sender, instance, created, **kwargs):
    'get or create a user profile'
    return UserProfile.objects.get_or_create(
        user=instance
    )



