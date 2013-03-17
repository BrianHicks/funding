'test methods on BalancedAccount model'
from django.contrib.auth.models import User
from django.test import TestCase
from itertools import product
from milkman.dairy import milkman
from nose import with_setup

from funding.apps.funding.models import BalancedAccount, \
    BalancedAccountManager, BalancedAccountTypes

def test_assigns_permissions():
    'fully_authorize assigns permissions'
    yield check_assigns_permissions, 'view'
    yield check_assigns_permissions, 'change'
    yield check_assigns_permissions, 'delete'

def check_assigns_permissions(perm):
    user = milkman.deliver(User)
    ba = milkman.deliver(BalancedAccount)
    ba.fully_authorize(user)

    perm = 'funding.%s_balancedaccount' % perm
    try:
        assert user.has_perm(perm, ba), \
            'user has no perm %s' % perm
    finally:
        user.delete()
        ba.delete()

def test_for_user():
    'test for_user on manager'
    kinds = dict(BalancedAccountTypes).keys()
    perms = ['view', 'change', 'delete']

    for kind, perm in product(kinds, perms):
        yield check_for_user, kind, perm

def check_for_user(kind, perm):
    user = milkman.deliver(User)
    ba = milkman.deliver(
        BalancedAccount, kind=kind, name=':'.join([kind, perm])
    )
    ba.fully_authorize(user)

    qs = BalancedAccount.objects.for_user(kind, perm, user)
    try:
        assert ba in qs, '%r not in %r' % (ba, qs)
    finally:
        user.delete()
        ba.delete()
