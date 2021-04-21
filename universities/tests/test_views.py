from django.test import Client, TestCase

from ..models import Major, University
from ..serializers import MajorSerializer01, UniversitySerializer01

client = Client()
BASE_URL = "/api/universities/"


class TestGetUniversitiesNameList(TestCase):
    # test request 200

    url = BASE_URL + "get-universities-name-list"

    def test_req(self):
        response = client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_res(self):
        university01 = University.objects.create()
        university02 = University.objects.create()

        # Asserting that view won't return this university
        University.objects.create(is_active=False)
        universities = [university01, university02]

        serializer = UniversitySerializer01(universities, many=True)

        response = client.get(self.url)
        self.assertEqual(response.data, serializer.data)


class TestGetMajorNameList(TestCase):
    url = BASE_URL + "get-majors-name-list"

    def test_req(self):
        response = client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_res(self):
        major01 = Major.objects.create()
        major02 = Major.objects.create()

        serializer = MajorSerializer01([major01, major02], many=True)

        response = client.get(self.url)
        self.assertEqual(response.data, serializer.data)
