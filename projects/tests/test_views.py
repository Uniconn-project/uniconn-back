from django.test import Client, TestCase
from rest_framework import status

from ..models import Market
from ..serializers import MarketSerializer01

client = Client()
BASE_URL = "/api/projects/"


class TestGetMarketsNameList(TestCase):
    url = BASE_URL + "get-markets-name-list"

    def test_req(self):
        response = client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_res(self):
        market01 = Market.objects.create()
        market02 = Market.objects.create()

        serializer = MarketSerializer01([market01, market02], many=True)

        response = client.get(self.url)
        self.assertEqual(response.data, serializer.data)
