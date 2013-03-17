'test methods on BalancedAccount model'
from django.contrib.auth.models import User
from django.test import TestCase

from funding.apps.funding.models import BalancedAccount, BalancedAccountsManager


class BalancedAccountTests(TestCase):
    'test for BalancedAccount'
    def setUp(self):
        'set up objects for testing'
        self.user = self.get_user()
        self.account = BalancedAccount.objects.create(
            kind='bank', name='test', uri='/test'
        )
        self.addCleanup(self.account.delete)

    def get_user(self, **user_kwargs):
        'get a user for testing'
        user_kwargs.setdefault('username', 'test')
        user_kwargs.setdefault('email', 'test@example.com')

        user = User.objects.create(**user_kwargs)
        self.addCleanup(user.delete)

        return user

    def test_fully_authorize_view(self):
        'fully_authorize adds view permission'
        self.account.fully_authorize(self.user)
        self.assertTrue(
            self.user.has_perm('funding.view_balancedaccount', self.account)
        )

    def test_fully_authorize_change(self):
        'fully_authorize adds change permission'
        self.account.fully_authorize(self.user)
        self.assertTrue(
            self.user.has_perm('funding.change_balancedaccount', self.account)
        )

    def test_fully_authorize_delete(self):
        'fully_authorize adds delete permission'
        self.account.fully_authorize(self.user)
        self.assertTrue(
            self.user.has_perm('funding.delete_balancedaccount', self.account)
        )
