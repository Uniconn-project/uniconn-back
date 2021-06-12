from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from projects.models import Project
from projects.serializers import ProjectSerializer01
from rest_framework import status

from ..models import Mentor, Profile, Student
from ..serializers import ProfileSerializer01, ProfileSerializer02, ProfileSerializer03

User = get_user_model()
client = Client()
BASE_URL = "/api/profiles/"


class TestSignupView(TestCase):
    pass


class TestGetMyProfile(TestCase):
    url = BASE_URL + "get-my-profile"

    def setUp(self):
        self.user01_STUDENT = User.objects.create(username="jeff")
        Student.objects.create(profile=self.user01_STUDENT.profile)

        self.user02_MENTOR = User.objects.create(username="larry")
        Mentor.objects.create(profile=self.user02_MENTOR.profile)

    def test_req(self):
        response = client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, "Login required view")

        client.force_login(self.user01_STUDENT)
        response = client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        client.force_login(self.user02_MENTOR)
        response = client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_res(self):
        student_serializer = ProfileSerializer01(self.user01_STUDENT.profile)
        mentor_serializer = ProfileSerializer02(self.user02_MENTOR.profile)

        client.force_login(self.user01_STUDENT)
        response = client.get(self.url)
        self.assertEqual(response.data, student_serializer.data)

        client.force_login(self.user02_MENTOR)
        response = client.get(self.url)
        self.assertEqual(response.data, mentor_serializer.data)


class TestGetProfile(TestCase):
    url = BASE_URL + "get-profile/"

    def setUp(self):
        self.user01_STUDENT = User.objects.create(username="jeff")
        Student.objects.create(profile=self.user01_STUDENT.profile)

        self.user02_MENTOR = User.objects.create(username="larry")
        Mentor.objects.create(profile=self.user02_MENTOR.profile)

    def test_req(self):
        response = client.get(self.url + "unexistent-username")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, "There isn't any user with such username")

        response = client.get(self.url + self.user01_STUDENT.username)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.get(self.url + self.user02_MENTOR.username)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_res(self):
        student_serializer = ProfileSerializer01(self.user01_STUDENT.profile)
        mentor_serializer = ProfileSerializer02(self.user02_MENTOR.profile)

        response = client.get(self.url + self.user01_STUDENT.username)
        self.assertEqual(response.data, student_serializer.data)

        response = client.get(self.url + self.user02_MENTOR.username)
        self.assertEqual(response.data, mentor_serializer.data)


class TestGetProfileProjects(TestCase):
    url = BASE_URL + "get-profile-projects/"

    def setUp(self):
        self.user01_STUDENT = User.objects.create(username="jeff")
        Student.objects.create(profile=self.user01_STUDENT.profile)

        self.user02_MENTOR = User.objects.create(username="larry")
        Mentor.objects.create(profile=self.user02_MENTOR.profile)

    def test_req(self):
        response = client.get(self.url + self.user01_STUDENT.username)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.get(self.url + self.user02_MENTOR.username)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_res(self):
        response = client.get(self.url + "unexistent-username")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, "There isn't any user with such username")

        project01 = Project.objects.create()
        project02 = Project.objects.create()
        project01.students.add(self.user01_STUDENT.profile.student)
        project02.students.add(self.user01_STUDENT.profile.student)
        serializer_STUDENT = ProjectSerializer01([project01, project02], many=True)

        project03 = Project.objects.create()
        project04 = Project.objects.create()
        project03.mentors.add(self.user02_MENTOR.profile.mentor)
        project04.mentors.add(self.user02_MENTOR.profile.mentor)
        serializer_MENTOR = ProjectSerializer01([project03, project04], many=True)

        response = client.get(self.url + self.user01_STUDENT.username)
        self.assertEqual(response.data, serializer_STUDENT.data)

        response = client.get(self.url + self.user02_MENTOR.username)
        self.assertEqual(response.data, serializer_MENTOR.data)


class TestGetFilteredProfiles(TestCase):
    url = BASE_URL + "get-filtered-profiles/"

    def setUp(self):
        pass

    def test_req(self):
        response = client.get(self.url + "")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response = client.get(self.url + "fel")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_res(self):
        User.objects.create(username="michael.JJ")
        User.objects.create(username="veronica")
        User.objects.create(username="jordan")
        User.objects.create(username="joanne")

        query = "j"
        response = client.get(self.url + query)
        self.assertEqual(len(response.data), 3)
        self.assertEqual(
            response.data, ProfileSerializer03(Profile.objects.filter(user__username__icontains=query), many=True).data
        )

        query = "JO"
        response = client.get(self.url + query)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(
            response.data, ProfileSerializer03(Profile.objects.filter(user__username__icontains=query), many=True).data
        )

        query = "joanne"
        response = client.get(self.url + query)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(
            response.data, ProfileSerializer03(Profile.objects.filter(user__username__icontains=query), many=True).data
        )

        query = "unexistent-username"
        response = client.get(self.url + query)
        self.assertEqual(len(response.data), 0)
        self.assertEqual(
            response.data, ProfileSerializer03(Profile.objects.filter(user__username__icontains=query), many=True).data
        )
