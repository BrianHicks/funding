'user test case'
from django.contrib.auth.models import User
from django.test import TestCase


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


