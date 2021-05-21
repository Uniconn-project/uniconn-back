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
