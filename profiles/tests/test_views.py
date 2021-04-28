from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from rest_framework import status

from ..models import Mentor, Profile, Student
from ..serializers import ProfileSerializer01, ProfileSerializer02

User = get_user_model()
client = Client()
BASE_URL = "/api/profiles/"


class TestSignupView(TestCase):
    pass


class TestGetMyProfile(TestCase):
    url_student = BASE_URL + "student/get-my-profile"
    url_mentor = BASE_URL + "mentor/get-my-profile"

    def setUp(self):
        self.user = User.objects.create(username="jeff")

    def test_req(self):
        response = client.get(self.url_student)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, "Login required view")

        response = client.get(self.url_mentor)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, "Login required view")

        client.force_login(self.user)
        response = client.get(self.url_student)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.get(self.url_mentor)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_res(self):
        # Creating both student and mentor objects using the same profile
        Student.objects.create(profile=self.user.profile)
        Mentor.objects.create(profile=self.user.profile)

        # Serializing the profile as a student (ProfileSerializer01) and as a mentor (ProfileSerializer02)
        student_serializer = ProfileSerializer01(self.user.profile)
        mentor_serializer = ProfileSerializer02(self.user.profile)

        client.force_login(self.user)
        response = client.get(self.url_student)
        self.assertEqual(response.data, student_serializer.data)

        response = client.get(self.url_mentor)
        self.assertEqual(response.data, mentor_serializer.data)
