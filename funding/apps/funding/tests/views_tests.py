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
    def tearDown(self):
        BankAccount.objects.all().delete()

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

    def test_post_associates_user(self):
        'post associates user with created BankAccount'
        self.client.post(
            reverse('funding:add'),
            data={
                'name': 'test_association',
                'uri': '/test'
            }
        )
        account = BankAccount.objects.get(name='test_association')

        self.assertTrue(self.user.has_perm('delete_bankaccount', account))

    def test_redirects(self):
        'redirects after successfully creating'
        response = self.client.post(
            reverse('funding:add'),
            data={
                'name': 'test_association',
                'uri': '/test'
            }
        )

        self.assertEqual(302, response.status_code)
        self.assertTrue(response['Location'].endswith(reverse('funding:list')))
