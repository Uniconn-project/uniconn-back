from django.test import Client, TestCase
from rest_framework import status

from ..models import Major, University
from ..serializers import MajorSerializer01, UniversitySerializer01

client = Client()
BASE_URL = "/api/universities/"


class TestGetUniversitiesNameList(TestCase):
    url = BASE_URL + "get-universities-name-list"

    def test_req(self):
        response = client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        for method in ["delete", "put", "patch", "post"]:
            response = getattr(client, method)(self.url)
            self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_res(self):
        university01 = University.objects.create()
        university02 = University.objects.create()
        # Asserting that view won't return this university
        University.objects.create(is_active=False)

        serializer = UniversitySerializer01([university01, university02], many=True)

        response = client.get(self.url)
        self.assertEqual(response.data, serializer.data)


class TestGetMajorNameList(TestCase):
    url = BASE_URL + "get-majors-name-list"

    def test_req(self):
        response = client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        for method in ["delete", "put", "patch", "post"]:
            response = getattr(client, method)(self.url)
            self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_res(self):
        major01 = Major.objects.create()
        major02 = Major.objects.create()

        serializer = MajorSerializer01([major01, major02], many=True)

        response = client.get(self.url)
        self.assertEqual(response.data, serializer.data)
