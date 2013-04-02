'tests for trips views'
from datetime import datetime
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from milkman.dairy import milkman

from funding.libs.usertest import UserTestCase

from ..models import Trip


class TripDetailViewTests(UserTestCase):
    'tests for TripDetailView'
    def setUp(self):
        'set up trip'
        super(TripDetailViewTests, self).setUp()
        self.trip = milkman.deliver(Trip)
        self.addCleanup(self.trip.delete)
        self.url = reverse('trips:detail', kwargs={'pk': self.trip.pk})
        self.trip.fully_authorize(self.user)

    def test_200_user(self):
        'succeeds for user'
        self.assertEqual(200, self.client.get(self.url).status_code)

    def test_200_anonymous(self):
        'succeeds for anonymous'
        self.client.logout()
        self.assertEqual(200, self.client.get(self.url).status_code)

    def test_no_post(self):
        'fails for POST'
        self.assertEqual(405, self.client.post(self.url).status_code)


class TripListViewTests(UserTestCase):
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

    def test_post_assigns_permissions(self):
        'POST assigns permissions'
        resp = self.client.post(
            reverse('trips:create'), data=self.get_trip_attrs()
        )
        latest = Trip.objects.latest('created_at')

        self.assertTrue(self.user.has_perm('trips.change_trip', latest))
        self.assertTrue(self.user.has_perm('trips.delete_trip', latest))


class TripUpdateViewTests(UserTestCase):
    'tests for TripUpdateView'
    def setUp(self):
        'set up trip'
        super(TripUpdateViewTests, self).setUp()
        self.trip = milkman.deliver(Trip)
        self.addCleanup(self.trip.delete)
        self.url = reverse('trips:update', kwargs={'pk': self.trip.pk})
        self.trip.fully_authorize(self.user)

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
        resp = self.client.get(self.url)

        self.assertEqual(302, resp.status_code)

    def test_302_post_logged_out(self):
        'redirects to login on POST if not logged in'
        self.client.logout()
        resp = self.client.post(self.url)

        self.assertEqual(302, resp.status_code)

    def test_200_get(self):
        'supports GET if logged in'
        resp = self.client.get(self.url)
        self.assertEqual(200, resp.status_code)

    def test_200_post(self):
        'updates Trip if logged in'
        attrs = self.get_trip_attrs()
        resp = self.client.post(self.url, data=attrs)
        new = Trip.objects.latest('updated_at')

        self.assertEqual(302, resp.status_code)
        self.assertNotEqual(self.trip.organization, attrs['organization'])
        self.assertEqual(new.organization, attrs['organization'])

    def test_200_post_other_user(self):
        'denies other user'
        self.client.logout()
        new = User.objects.create_user(
            username='other', password='test', email='a@b.com'
        )
        self.addCleanup(new.delete)
        self.client.login(username='other', password='test')

        attrs = self.get_trip_attrs()
        resp = self.client.post(self.url, data=attrs)
        new = Trip.objects.latest('updated_at')

        self.assertEqual(404, resp.status_code)
        self.assertNotEqual(new.organization, attrs['organization'])

    def test_post_redirects_to_list(self):
        'POST redirects to list on success'
        resp = self.client.post(self.url, data=self.get_trip_attrs())

        self.assertEqual(302, resp.status_code)
        self.assertEqual(None, resp.context)
        self.assertTrue(resp['location'].endswith(reverse('trips:list')))


class TripDeleteViewTests(UserTestCase):
    'tests for TripDeleteView'
    def setUp(self):
        'set up trip'
        super(TripDeleteViewTests, self).setUp()
        self.trip = milkman.deliver(Trip)
        self.addCleanup(self.trip.delete)
        self.url = reverse('trips:delete', kwargs={'pk': self.trip.pk})
        self.trip.fully_authorize(self.user)

    def test_302_logged_out(self):
        'redirects to login if not logged in'
        self.client.logout()
        resp = self.client.get(self.url)

        self.assertEqual(302, resp.status_code)

    def test_302_post_logged_out(self):
        'redirects to login on POST if not logged in'
        self.client.logout()
        resp = self.client.post(self.url)

        self.assertEqual(302, resp.status_code)

    def test_200_get(self):
        'supports GET if logged in'
        resp = self.client.get(self.url)
        self.assertEqual(200, resp.status_code)

    def test_200_post(self):
        'deletes Trip if logged in'
        resp = self.client.post(self.url)

        self.assertEqual(302, resp.status_code)
        self.assertEqual(0, Trip.objects.filter(id=self.trip.id).count())

    def test_200_post_other_user(self):
        'denies other user'
        self.client.logout()
        new = User.objects.create_user(
            username='other', password='test', email='a@b.com'
        )
        self.addCleanup(new.delete)
        self.client.login(username='other', password='test')

        resp = self.client.post(self.url)

        self.assertEqual(404, resp.status_code)
        self.assertEqual(1, Trip.objects.filter(id=self.trip.id).count())

    def test_post_redirects_to_list(self):
        'POST redirects to list on success'
        resp = self.client.post(self.url)

        self.assertEqual(302, resp.status_code)
        self.assertEqual(None, resp.context)
        self.assertTrue(resp['location'].endswith(reverse('trips:list')))
