from django.test import TestCase
from django.urls import resolve

from ..views import *

BASE_URL = "/api/universities/"


class TestUrls(TestCase):
    def test_get_universities_name_list_url(self):
        self.assertEqual(resolve(BASE_URL + "get-universities-name-list").func, get_universities_name_list)

    def test_get_majors_name_list_url(self):
        self.assertEqual(resolve(BASE_URL + "get-majors-name-list").func, get_majors_name_list)
