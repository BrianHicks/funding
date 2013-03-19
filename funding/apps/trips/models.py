'models for Trips'
from django.db import models
from guardian.shortcuts import assign, get_objects_for_user

from django.contrib.auth.models import User


class TripManager(models.Manager):
    'manager for Trips'
    def for_user(self, perm, user):
        'return a list of objects the user has permission for'
        return get_objects_for_user(
            user, 'trips.%s_trip' % perm
        )


class Trip(models.Model):
    'a missions trip or project'
    # internal representation of this data
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # public representation
    user = models.ForeignKey(User)
    what = models.TextField(help_text='What will you be doing?')
    where = models.CharField(
        max_length=140, help_text='Where will you be going?'
    )
    when = models.DateTimeField(help_text='When is your goal?')
    organization = models.CharField(
        max_length=140, help_text='Who are you going with?'
    )

    # money
    amount_needed = models.DecimalField(
        max_digits=7, decimal_places=2,
        help_text='How much do you need to raise?'
    )
    due = models.DateTimeField(
        help_text='When do you need to have all the money?'
    )

    # optional fields
    testimony = models.TextField(
        blank=True, help_text='Give a short testimony - why are you going?'
    )

    objects = TripManager()

    def fully_authorize(self, user):
        'fully authorize a user to change this trip'
        assign('change_trip', user, self)
        assign('delete_trip', user, self)

    def __unicode__(self):
        return "%s's trip to %s" % (self.user, self.where)
