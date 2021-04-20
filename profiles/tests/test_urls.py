from django.test import TestCase
from django.urls import resolve

from ..views import *

BASE_URL = "/api/profiles/"


class TestUrls(TestCase):
    def test_post_signup_url(self):
        self.assertEqual(resolve(BASE_URL + "student/post-signup").func, signup_view)
