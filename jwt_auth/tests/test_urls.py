from django.test import TestCase
from django.urls import resolve

from ..views import *

BASE_URL = "/token/"


class TestUrls(TestCase):
    def test_login_url(self):
        self.assertEqual(resolve(BASE_URL).view_name, "jwt_auth.views.Login")

    def test_refresh_url(self):
        self.assertEqual(resolve(BASE_URL + "refresh/").view_name, "jwt_auth.views.RefreshToken")

    def test_logout_url(self):
        self.assertEqual(resolve(BASE_URL + "logout/").view_name, "jwt_auth.views.Logout")
