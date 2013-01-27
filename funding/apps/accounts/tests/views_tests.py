'tests for accounts views'
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase


class ReceiverAddAccountViewTests(TestCase):
    'test ReceiverAddAccountView'
    def setUp(self):
        'add a user'
        self.user = User.objects.create_user(
            username='test',
            password='test'
        )
        self.addCleanup(self.user.delete)

        self.client.login(username='test', password='test')

    def test_returns_200(self):
        'returns 200 for authenticated user'
        response = self.client.get(reverse('accounts:funding:add'))
        self.assertEqual(200, response.status_code)

    def test_returns_404(self):
        'returns 404 for an unauthorized user'
        self.client.logout()
        response = self.client.get(reverse('accounts:funding:add'))
        self.assertEqual(302, response.status_code)
