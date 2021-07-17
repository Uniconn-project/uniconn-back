from django.test import TestCase
from django.urls import resolve

from ..views import *

BASE_URL = "/api/profiles/"


class TestUrls(TestCase):
    def test_post_signup_url(self):
        self.assertEqual(resolve(BASE_URL + "student/post-signup").func, signup_view)
        self.assertEqual(resolve(BASE_URL + "mentor/post-signup").func, signup_view)

    def test_edit_my_profile_url(self):
        self.assertEqual(resolve(BASE_URL + "edit-my-profile").func, edit_my_profile)

    def test_get_my_profile_url(self):
        self.assertEqual(resolve(BASE_URL + "get-my-profile").func, get_my_profile)

    def test_get_profile_url(self):
        self.assertEqual(resolve(BASE_URL + "get-profile/alicia").func, get_profile)

    def test_get_profile_projects_url(self):
        self.assertEqual(resolve(BASE_URL + "get-profile-projects/alicia").func, get_profile_projects)

    def test_get_mentor_markets_url(self):
        self.assertEqual(resolve(BASE_URL + "get-mentor-markets/alicia").func, get_mentor_markets)

    def test_get_filtered_profiles_url(self):
        self.assertEqual(resolve(BASE_URL + "get-filtered-profiles/ali").func, get_filtered_profiles)

    def test_get_profile_list_url(self):
        self.assertEqual(resolve(BASE_URL + "get-profile-list").func, get_profile_list)

    def test_get_skills_name_list_url(self):
        self.assertEqual(resolve(BASE_URL + "get-skills-name-list").func, get_skills_name_list)

    def test_get_notifications_url(self):
        self.assertEqual(resolve(BASE_URL + "get-notifications").func, get_notifications)

    def test_get_notifications_number_url(self):
        self.assertEqual(resolve(BASE_URL + "get-notifications-number").func, get_notifications_number)

    def test_visualize_notifications_url(self):
        self.assertEqual(resolve(BASE_URL + "visualize-notifications").func, visualize_notifications)
