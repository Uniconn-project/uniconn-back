from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from rest_framework import status

User = get_user_model()
client = Client()
BASE_URL = "/token/"


class TestLoginView(TestCase):
    url = BASE_URL + ""

    def test_req(self):
        response = client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        for method in ["get", "delete", "put", "patch"]:
            response = getattr(client, method)(self.url)
            self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_res(self):
        user = User.objects.create(username="john.doe")
        user.set_password("secret")
        user.save()

        response = client.post(self.url, {"password": "secret"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"username": ["This field is required."]})

        response = client.post(self.url, {"username": "john.doe"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"password": ["This field is required."]})

        post_data = {"username": "john.doe", "password": "secret"}

        # blank username
        response = client.post(self.url, {**post_data, "username": ""})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"username": ["This field may not be blank."]})

        # blank password
        response = client.post(self.url, {**post_data, "password": ""})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"password": ["This field may not be blank."]})

        # wrong username
        response = client.post(self.url, {**post_data, "username": "john.doee"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {"detail": "No active account found with the given credentials"})

        # wrong password
        response = client.post(self.url, {**post_data, "password": "secretttt"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {"detail": "No active account found with the given credentials"})

        # successful login
        response = client.post(self.url, post_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(list(response.data.keys()), ["refresh", "access", "refresh_expires", "access_expires"])


class TestRefreshView(TestCase):
    pass


class TestLogoutView(TestCase):
    pass
