from django.test import TestCase
from django.urls import resolve

from ..views import *

BASE_URL = "/api/projects/"


class TestUrls(TestCase):
    def test_get_markets_name_list_url(self):
        self.assertEqual(resolve(BASE_URL + "get-markets-name-list").func, get_markets_name_list)

    def test_get_projects_list_url(self):
        self.assertEqual(resolve(BASE_URL + "get-projects-list").func, get_projects_list)

    def test_get_filtered_projects_list_url(self):
        self.assertEqual(resolve(BASE_URL + "get-filtered-projects-list").func, get_filtered_projects_list)

    def test_get_projects_categories_list_url(self):
        self.assertEqual(resolve(BASE_URL + "get-projects-categories-list").func, get_projects_categories_list)

    def test_create_project_url(self):
        self.assertEqual(resolve(BASE_URL + "create-project").func, create_project)

    def test_get_project_url(self):
        self.assertEqual(resolve(BASE_URL + "get-project/2").func, get_project)

    def test_edit_project_url(self):
        self.assertEqual(resolve(BASE_URL + "edit-project/4").func, edit_project)

    def test_invite_to_project_url(self):
        self.assertEqual(resolve(BASE_URL + "invite-students-to-project/1").func, invite_users_to_project)
        self.assertEqual(resolve(BASE_URL + "invite-mentors-to-project/1").func, invite_users_to_project)

    def test_edit_project_description_url(self):
        self.assertEqual(resolve(BASE_URL + "edit-project-description/918").func, edit_project_description)

    def test_create_link_url(self):
        self.assertEqual(resolve(BASE_URL + "create-link/10").func, create_link)
