from django.test import TestCase
from django.urls import resolve

from ..views import *

BASE_URL = "/api/profiles/"


class TestUrls(TestCase):
    def test_post_signup_url(self):
        self.assertEqual(resolve(BASE_URL + "student/post-signup").func, signup_view)

    def test_get_my_profile_url(self):
        self.assertEqual(resolve(BASE_URL + "get-my-profile").func, get_my_profile)

    def test_get_profile_url(self):
        self.assertEqual(resolve(BASE_URL + "get-profile/elon").func, get_profile)

    def test_get_profile_projects_url(self):
        self.assertEqual(resolve(BASE_URL + "get-profile-projects/alicia").func, get_profile_projects)

    def test_get_filtered_profiles_url(self):
        self.assertEqual(resolve(BASE_URL + "get-filtered-profiles/ali").func, get_filtered_profiles)

    def test_get_profile_list(self):
        self.assertEqual(resolve(BASE_URL + "get-profile-list").func, get_profile_list)
