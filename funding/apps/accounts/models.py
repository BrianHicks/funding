from django.contrib.auth.models import User
from django.db import models
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

def get_or_create_user_profile(request):
    profile = None
    user = request.user
    try:
        profile = user.get_profile()
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=user)
    return profile
