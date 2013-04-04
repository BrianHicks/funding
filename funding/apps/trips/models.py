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


trip_letter_help = "Write your support letter. A good letter includes most of " + \
    "the following: where you're going, who you're going with, what you'll " + \
    "be doing once you arrive, and a short testimony."

trip_money_explanation_help = "Explain what money you need and what it will " + \
    "go towards. This is also a good place to mention special needs for " + \
    "this trip: what should people be praying for?"

class Trip(models.Model):
    'a missions trip or project'
    # internal representation of this data
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # public representation
    user = models.ForeignKey(User)
    letter = models.TextField(help_text=trip_letter_help)
    where = models.CharField(max_length=140, help_text='Where are you going?')
    when = models.CharField(max_length=140, help_text='When do you leave?')
    video = models.CharField(
        max_length=140, blank=True,
        help_text='Personalize your trip page with a video about your trip. Copy a video URL in this field and we will do our best to display it properly.'
    )

    # money
    money_explanation = models.TextField(help_text=trip_money_explanation_help)
    amount_needed = models.DecimalField(
        max_digits=7, decimal_places=2,
        help_text='How much do you need to raise?'
    )
    due = models.DateTimeField(
        help_text='When do you need to have all the money?'
    )

    objects = TripManager()

    def fully_authorize(self, user):
        'fully authorize a user to change this trip'
        assign('change_trip', user, self)
        assign('delete_trip', user, self)

    def __unicode__(self):
        return "%s's trip to %s" % (self.user, self.where)
