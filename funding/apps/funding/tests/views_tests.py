'tests for accounts views'
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from guardian.shortcuts import assign

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


class BankAccountAddViewTests(UserTestCase):
    'test BankAccountAddView'
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


class BankAccountListViewTests(UserTestCase):
    'tests for BankAccountListView'
    def test_returns_404(self):
        'returns 404 for an unauthorized user'
        self.client.logout()
        response = self.client.get(reverse('funding:list'))
        self.assertEqual(302, response.status_code)

    def test_lists_owned_objects(self):
        'returns a list of owned objects, without unowned objects'
        yes = BankAccount.objects.create(name='yes', uri='yes')
        no = BankAccount.objects.create(name='no', uri='no')

        self.addCleanup(yes.delete)
        self.addCleanup(no.delete)

        assign('view_bankaccount', self.user, yes)

        response = self.client.get(reverse('funding:list'))

        self.assertEqual(
            [yes],
            list(response.context['bankaccount_list'])
        )


class BankAccountDeleteViewTests(UserTestCase):
    'test deleting'
    def setUp(self):
        self.ba = BankAccount.objects.create(name='test', uri='test')
        self.addCleanup(self.ba.delete)
        super(BankAccountDeleteViewTests, self).setUp()

    def test_get_302(self):
        'GET is a 404 if not logged in'
        self.client.logout()
        response = self.client.get(reverse(
            'funding:delete', kwargs={'pk': self.ba.pk}
        ))
        self.assertEqual(302, response.status_code)

    def test_get_404_not_authorized(self):
        'GET is a 404 if not authorized'
        response = self.client.get(reverse(
            'funding:delete', kwargs={'pk': self.ba.pk}
        ))
        self.assertEqual(404, response.status_code)

    def test_get_200_authorized(self):
        'GET is 200 if authorized'
        assign('delete_bankaccount', self.user, self.ba)
        response = self.client.get(reverse(
            'funding:delete', kwargs={'pk': self.ba.pk}
        ))
        self.assertEqual(200, response.status_code)

    def test_post_404_unauthorized(self):
        'POST is 404 if unauthorized'
        response = self.client.get(reverse(
            'funding:delete', kwargs={'pk': self.ba.pk}
        ))
        self.assertEqual(404, response.status_code)

    def test_post_302_authorized(self):
        'POST is 302 if authorized'
        assign('delete_bankaccount', self.user, self.ba)
        response = self.client.post(reverse(
            'funding:delete', kwargs={'pk': self.ba.pk}
        ))
        self.assertEqual(302, response.status_code)
        self.assertTrue(response['Location'].endswith(reverse('funding:list')))