from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from django.utils.translation import ugettext as _
from userena.models import UserenaBaseProfile


class UserProfile(UserenaBaseProfile):
    'User Profile'
    user = models.OneToOneField(
        User,
        unique=True,
        verbose_name=_('user'),
        related_name='profile',
    )


@receiver(models.signals.post_save, sender=User)
def get_or_create_user_profile(sender, instance, created, **kwargs):
    'get or create a user profile'
    return UserProfile.objects.get_or_create(
        user=instance
    )


# Balanced Payments models
class BankAccount(models.Model):
    'represent a balanced bank account'
    name = models.CharField(max_length=100)
    uri = models.CharField(max_length=500)
