from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from projects.models import (
    Discussion,
    DiscussionReply,
    DiscussionStar,
    Project,
    ProjectEnteringRequest,
)
from projects.serializers import (
    DiscussionReplySerializer02,
    DiscussionStarSerializer02,
    MarketSerializer01,
    ProjectEnteringRequestSerializer01,
    ProjectSerializer01,
    ProjectSerializer03,
)
from rest_framework import status

from ..models import Mentor, Profile, Student
from ..serializers import ProfileSerializer01, ProfileSerializer02, ProfileSerializer03

User = get_user_model()
client = Client()
BASE_URL = "/api/profiles/"


class TestSignupView(TestCase):
    pass


class TestEditMyProfileView(TestCase):
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
        self.assertEqual(response.data, "Você precisa logar para acessar essa rota")

        client.force_login(self.user01_STUDENT)
        response = client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        client.force_login(self.user02_MENTOR)
        response = client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        for method in ["delete", "put", "patch", "post"]:
            response = getattr(client, method)(self.url)
            self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

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

        for method in ["delete", "put", "patch", "post"]:
            response = getattr(client, method)(self.url + self.user01_STUDENT.username)
            self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

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

        for method in ["delete", "put", "patch", "post"]:
            response = getattr(client, method)(self.url + self.user02_MENTOR.username)
            self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_res(self):
        response = client.get(self.url + "unexistent-username")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, "There isn't any user with such username")

        project01 = Project.objects.create()
        project02 = Project.objects.create()
        project01.students.add(self.user01_STUDENT.profile.student)
        project02.students.add(self.user01_STUDENT.profile.student)
        serializer_STUDENT = ProjectSerializer01([project02, project01], many=True)

        project03 = Project.objects.create()
        project04 = Project.objects.create()
        project03.mentors.add(self.user02_MENTOR.profile.mentor)
        project04.mentors.add(self.user02_MENTOR.profile.mentor)
        serializer_MENTOR = ProjectSerializer01([project04, project03], many=True)

        response = client.get(self.url + self.user01_STUDENT.username)
        self.assertEqual(response.data, serializer_STUDENT.data)

        response = client.get(self.url + self.user02_MENTOR.username)
        self.assertEqual(response.data, serializer_MENTOR.data)


class TestGetMentorMarkets(TestCase):
    url = BASE_URL + "get-mentor-markets/"

    def test_req(self):
        response = client.get(self.url + "phil")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        user = User.objects.create(username="phil")

        response = client.get(self.url + "phil")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        Mentor.objects.create(profile=user.profile)

        response = client.get(self.url + "phil")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        for method in ["delete", "put", "patch", "post"]:
            response = getattr(client, method)(self.url + "phil")
            self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_res(self):
        response = client.get(self.url + "phil")
        self.assertEqual(response.data, "There isn't any user with such username")

        user = User.objects.create(username="phil")

        response = client.get(self.url + "phil")
        self.assertEqual(response.data, "Only mentors have markets")

        mentor = Mentor.objects.create(profile=user.profile)

        response = client.get(self.url + "phil")
        self.assertEqual(response.data, MarketSerializer01(mentor.markets.all(), many=True).data)


class TestGetFilteredProfiles(TestCase):
    url = BASE_URL + "get-filtered-profiles/"

    def test_req(self):
        response = client.get(self.url + "")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response = client.get(self.url + "fel")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        for method in ["delete", "put", "patch", "post"]:
            response = getattr(client, method)(self.url + "feli")
            self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

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


class TestGetProfileList(TestCase):
    url = BASE_URL + "get-profile-list"

    def test_req(self):
        response = client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        for method in ["delete", "put", "patch", "post"]:
            response = getattr(client, method)(self.url)
            self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_res(self):
        profiles = []

        for i in range(15):
            user = User.objects.create(username=f"user0{i}")
            profiles.append(user.profile)

        response = client.get(self.url)
        self.assertEqual(response.data, ProfileSerializer03(profiles[:10], many=True).data)


class TestGetNotifications(TestCase):
    url = BASE_URL + "get-notifications"

    def test_req(self):
        response = client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        for method in ["delete", "put", "patch", "post"]:
            response = getattr(client, method)(self.url)
            self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_res(self):
        user = User.objects.create(username="felipe")
        client.force_login(user)

        profile01 = User.objects.create(username="peter").profile
        Student.objects.create(profile=profile01)
        profile02 = User.objects.create(username="jane").profile
        Mentor.objects.create(profile=profile02)

        project01 = Project.objects.create()
        project02 = Project.objects.create()
        project03 = Project.objects.create()

        discussion01 = Discussion.objects.create(profile=user.profile, project=project01)
        discussion02 = Discussion.objects.create(profile=user.profile, project=project02)

        project_entering_request01 = ProjectEnteringRequest.objects.create(project=project01, profile=profile01)
        project_entering_request02 = ProjectEnteringRequest.objects.create(project=project01, profile=profile02)

        response = client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, "Dados inválidos!")

        student = Student.objects.create(profile=user.profile)

        response = client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {
                "projects_invitations": [],
                "projects_entering_requests": [],
                "discussions_stars": [],
                "discussions_replies": [],
            },
        )

        project01.students.add(student)
        project01.save()

        project02.pending_invited_students.add(student)
        project02.save()
        project03.pending_invited_students.add(student)
        project03.save()

        discussion_star01 = DiscussionStar.objects.create(discussion=discussion01, profile=profile01)
        discussion_star02 = DiscussionStar.objects.create(discussion=discussion01, profile=profile02)
        discussion_star03 = DiscussionStar.objects.create(discussion=discussion02, profile=profile01)

        discussion_reply01 = DiscussionReply.objects.create(discussion=discussion01, profile=profile01)
        discussion_reply02 = DiscussionReply.objects.create(discussion=discussion01, profile=profile02)
        discussion_reply03 = DiscussionReply.objects.create(discussion=discussion02, profile=profile01)

        response = client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {
                "projects_invitations": ProjectSerializer03([project03, project02], many=True).data,
                "projects_entering_requests": ProjectEnteringRequestSerializer01(
                    [project_entering_request02, project_entering_request01], many=True
                ).data,
                "discussions_stars": DiscussionStarSerializer02(
                    [discussion_star03, discussion_star02, discussion_star01], many=True
                ).data,
                "discussions_replies": DiscussionReplySerializer02(
                    [discussion_reply03, discussion_reply02, discussion_reply01], many=True
                ).data,
            },
        )

        student.delete()
        mentor = Mentor.objects.create(profile=user.profile)

        response = client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {
                "projects_invitations": [],
                "projects_entering_requests": [],
                "discussions_stars": DiscussionStarSerializer02(
                    [discussion_star03, discussion_star02, discussion_star01], many=True
                ).data,
                "discussions_replies": DiscussionReplySerializer02(
                    [discussion_reply03, discussion_reply02, discussion_reply01], many=True
                ).data,
            },
        )

        project01.mentors.add(mentor)
        project02.pending_invited_mentors.add(mentor)
        project02.save()
        project03.pending_invited_mentors.add(mentor)
        project03.save()

        response = client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {
                "projects_invitations": ProjectSerializer03([project03, project02], many=True).data,
                "projects_entering_requests": [],
                "discussions_stars": DiscussionStarSerializer02(
                    [discussion_star03, discussion_star02, discussion_star01], many=True
                ).data,
                "discussions_replies": DiscussionReplySerializer02(
                    [discussion_reply03, discussion_reply02, discussion_reply01], many=True
                ).data,
            },
        )


class TestGetNotificationsNumber(TestCase):
    pass


class TestVisualizeNotifications(TestCase):
    url = BASE_URL + "visualize-notifications"

    def test_req(self):
        response = client.patch(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        for method in ["get", "delete", "post", "put"]:
            response = getattr(client, method)(self.url)
            self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_res(self):
        user = User.objects.create()
        client.force_login(user)

        response = client.patch(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, "success")

        discussion = Discussion.objects.create(profile=user.profile)
        discussion_star01 = DiscussionStar.objects.create(discussion=discussion)
        discussion_star02 = DiscussionStar.objects.create(discussion=discussion)

        self.assertFalse(discussion_star01.visualized)
        self.assertFalse(discussion_star02.visualized)

        response = client.patch(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, "success")

        discussion_star01.refresh_from_db()
        discussion_star02.refresh_from_db()

        self.assertTrue(discussion_star01.visualized)
        self.assertTrue(discussion_star02.visualized)
