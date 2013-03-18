'tests for accounts views'
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase

from funding.apps.funding.models import BalancedAccount
from funding.libs.usertest import UserTestCase


class BalancedAccountAddViewTests(UserTestCase):
    'test BalancedAccountAddView'
    def tearDown(self):
        BalancedAccount.objects.all().delete()

    def test_returns_200(self):
        'returns 200 for authenticated user'
        response = self.client.get(reverse('funding:add'))
        self.assertEqual(200, response.status_code)

    def test_returns_404(self):
        'returns 404 for an unauthorized user'
        self.client.logout()
        response = self.client.get(reverse('funding:add'))
        self.assertEqual(302, response.status_code)

    def test_post_creates_balancedaccount(self):
        'post creates a BalancedAccount'
        count = BalancedAccount.objects.count()
        response = self.client.post(
            reverse('funding:add'),
            data={
                'name': 'Test',
                'uri': '/test'
            }
        )
        self.assertEqual(count + 1, BalancedAccount.objects.count())

    def test_post_associates_user(self):
        'post associates user with created BalancedAccount'
        self.client.post(
            reverse('funding:add'),
            data={
                'name': 'test_association',
                'uri': '/test'
            }
        )
        account = BalancedAccount.objects.get(name='test_association')

        self.assertTrue(self.user.has_perm('delete_balancedaccount', account))

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


class BalancedAccountListViewTests(UserTestCase):
    'tests for BalancedAccountListView'
    def test_returns_404(self):
        'returns 404 for an unauthorized user'
        self.client.logout()
        response = self.client.get(reverse('funding:list'))
        self.assertEqual(302, response.status_code)

    def test_lists_owned_objects(self):
        'returns a list of owned objects, without unowned objects'
        yes = BalancedAccount.objects.create(name='yes', uri='yes', kind='bank')
        no = BalancedAccount.objects.create(name='no', uri='no', kind='bank')

        self.addCleanup(yes.delete)
        self.addCleanup(no.delete)

        yes.fully_authorize(self.user)

        response = self.client.get(reverse('funding:list'))

        self.assertEqual(
            [yes],
            list(response.context['balancedaccount_list'])
        )


class BalancedAccountDeleteViewTests(UserTestCase):
    'test deleting'
    def setUp(self):
        self.ba = BalancedAccount.objects.create(name='test', uri='test', kind='bank')
        self.addCleanup(self.ba.delete)
        super(BalancedAccountDeleteViewTests, self).setUp()

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
        self.ba.fully_authorize(self.user)
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
        self.ba.fully_authorize(self.user)
        response = self.client.post(reverse(
            'funding:delete', kwargs={'pk': self.ba.pk}
        ))
        self.assertEqual(302, response.status_code)
        self.assertTrue(response['Location'].endswith(reverse('funding:list')))
