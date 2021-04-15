from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Profile

User = get_user_model()


class TestSignals(TestCase):
    def setUp(self):
        pass

    def test_create_profile_signal(self):
        user = User.objects.create()

        self.assertEqual(Profile.objects.first(), user.profile)
