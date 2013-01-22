from django.test import TestCase


class HomepageTest(TestCase):
    'tests for homepage'
    def test_location(self):
        'test that HomepageView is located at /'
        resp = self.client.get('/')

        self.assertEqual(['homepage.html'], [t.name for t in resp.templates])
        self.assertEqual(200, resp.status_code)
