from django.db import models
from guardian.shortcuts import assign

from funding.libs.choices import Choice

# Balanced Payments models
class BalancedAccountTypes(Choice):
    BANK_ACCOUNT = 'bank'
    CREDIT_CARD = 'card'


class BalancedAccountsManager(models.Manager):
    'managed for BalancedAccount objects'


class BalancedAccount(models.Model):
    'represent a balanced bank account'
    kind = models.CharField(max_length=4, choices=BalancedAccountTypes)
    name = models.CharField(max_length=100)
    uri = models.CharField(max_length=500)

    objects = BalancedAccountsManager()

    def fully_authorize(self, user):
        'authorize a user to view and modify this account'
        assign('view_balancedaccount', user, self)
        assign('change_balancedaccount', user, self)
        assign('delete_balancedaccount', user, self)

    class Meta:
        permissions = (
            ('view_balancedaccount', 'View Account'),
        )

    def __unicode__(self):
        return self.name
