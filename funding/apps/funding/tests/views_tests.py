'tests for accounts views'
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase

from funding.apps.funding.models import BankAccount


class UserTestCase(TestCase):
    'test with a user'
    def setUp(self):
        'add a user'
        self.user = User.objects.create_user(
            username='test',
            password='test'
        )
        self.addCleanup(self.user.delete)

        self.client.login(username='test', password='test')


class ReceiverAddAccountViewTests(UserTestCase):
    'test ReceiverAddAccountView'
    def test_returns_200(self):
        'returns 200 for authenticated user'
        response = self.client.get(reverse('funding:add'))
        self.assertEqual(200, response.status_code)

    def test_returns_404(self):
        'returns 404 for an unauthorized user'
        self.client.logout()
        response = self.client.get(reverse('funding:add'))
        self.assertEqual(302, response.status_code)

    def test_post_creates_bankaccount(self):
        'post creates a BankAccount'
        count = BankAccount.objects.count()
        response = self.client.post(
            reverse('funding:add'),
            data={
                'name': 'Test',
                'uri': '/test'
            }
        )
        self.assertEqual(count + 1, BankAccount.objects.count())
