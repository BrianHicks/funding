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
    balanced_id = models.CharField(max_length=100)
    fingerprint = models.CharField(max_length=25)
    is_valid = models.BooleanField(default=True)

    bank_code = models.CharField(max_length=25)
    bank_name = models.CharField(max_length=100)
    account_number = models.CharField(max_length=50)
    routing_number = models.CharField(max_length=50)
    account_type = models.CharField(max_length=10)
    last_four = models.CharField(max_length=4)
    name = models.CharField(max_length=100)

    uri = models.CharField(max_length=500)
    credits_uri = models.CharField(max_length=500)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
