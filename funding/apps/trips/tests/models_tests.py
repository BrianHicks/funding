'test Trip model'
from django.contrib.auth.models import User
from django.test import TestCase
from itertools import product
from milkman.dairy import milkman

from funding.apps.trips.models import Trip

def test_assigns_permissions():
    'fully_authorize assigns permissions'
    yield check_assigns_permissions, 'change'
    yield check_assigns_permissions, 'delete'

def check_assigns_permissions(perm):
    user = milkman.deliver(User)
    trip = milkman.deliver(Trip)
    trip.fully_authorize(user)

    perm = 'trips.%s_trip' % perm
    try:
        assert user.has_perm(perm, trip), \
            'user has no perm %s' % perm
    finally:
        user.delete()
        trip.delete()

def test_for_user():
    'test for_user on manager'
    perms = ['change', 'delete']

    for perm in perms:
        yield check_for_user, perm

def check_for_user(perm):
    user = milkman.deliver(User)
    trip = milkman.deliver(
        Trip, name=perm
    )
    trip.fully_authorize(user)

    qs = Trip.objects.for_user(perm, user)
    try:
        assert trip in qs, '%r not in %r' % (trip, qs)
    finally:
        user.delete()
        trip.delete()
