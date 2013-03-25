'tests for trips views'
from datetime import datetime
from django.core.urlresolvers import reverse
from milkman.dairy import milkman

from funding.libs.usertest import UserTestCase

from ..models import Trip


class TripListViewTest(UserTestCase):
    'tests for TripListView'
    def test_302_logged_out(self):
        'redirects to login if not logged in'
        self.client.logout()
        resp = self.client.get(reverse('trips:list'))

        self.assertEqual(302, resp.status_code)

    def test_405_post(self):
        'list does not support post'
        resp = self.client.post(reverse('trips:list'))
        self.assertEqual(405, resp.status_code)

    def test_200_get(self):
        'supports GET if logged in'
        resp = self.client.get(reverse('trips:list'))
        self.assertEqual(200, resp.status_code)

    def test_has_correct_objects(self):
        'has correct objects for user (those which can be modified)'
        yes = milkman.deliver(Trip, where='Yesland', user=self.user)
        no = milkman.deliver(Trip, where='Nopeland', user=self.user)

        yes.fully_authorize(self.user)

        resp = self.client.get(reverse('trips:list'))

        self.assertIn(yes, resp.context['trip_list'])
        self.assertNotIn(no, resp.context['trip_list'])


class TripCreateViewTests(UserTestCase):
    'tests for TripCreateView'
    def get_trip_attrs(self):
        'get trip attrs'
        return {
            'what': 'what',
            'when': datetime.now().strftime('%Y-%m-%d'),
            'due': datetime.now().strftime('%Y-%m-%d'),
            'user': self.user,
            'organization': 'organization',
            'where': 'where',
            'amount_needed': 50.00
        }

    def test_302_logged_out(self):
        'redirects to login if not logged in'
        self.client.logout()
        resp = self.client.get(reverse('trips:create'))

        self.assertEqual(302, resp.status_code)

    def test_302_post_logged_out(self):
        'redirects to login on POST if not logged in'
        self.client.logout()
        resp = self.client.post(reverse('trips:create'))

        self.assertEqual(302, resp.status_code)

    def test_200_get(self):
        'supports GET if logged in'
        resp = self.client.get(reverse('trips:create'))
        self.assertEqual(200, resp.status_code)

    def test_200_post(self):
        'creates Trip if logged in'
        count = Trip.objects.count()
        resp = self.client.post(
            reverse('trips:create'), data=self.get_trip_attrs()
        )

        self.assertEqual(302, resp.status_code)
        self.assertEqual(None, resp.context)
        self.assertEqual(count + 1, Trip.objects.count())

    def test_post_with_user(self):
        'associates the new trip with the POSTing user'
        resp = self.client.post(
            reverse('trips:create'), data=self.get_trip_attrs()
        )

        self.assertEqual(self.user, Trip.objects.latest('created_at').user)
        self.assertEqual(None, resp.context)
        self.assertEqual(302, resp.status_code)

    def test_post_redirects_to_list(self):
        'POST redirects to list on success'
        resp = self.client.post(
            reverse('trips:create'), data=self.get_trip_attrs()
        )

        self.assertEqual(302, resp.status_code)
        self.assertEqual(None, resp.context)
        self.assertTrue(resp['location'].endswith(reverse('trips:list')))
