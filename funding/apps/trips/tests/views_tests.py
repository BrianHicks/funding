'tests for trips views'
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
