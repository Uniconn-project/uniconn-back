from django.test import Client, TestCase
from rest_framework import status

from ..models import Market, Project
from ..serializers import MarketSerializer01, ProjectSerializer01, ProjectSerializer02

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


class TestGetProjectsList(TestCase):
    url = BASE_URL + "get-projects-list"

    def test_req(self):
        response = client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_res(self):
        project01 = Project.objects.create()
        project02 = Project.objects.create()

        serializer = ProjectSerializer01([project01, project02], many=True)

        response = client.get(self.url)
        self.assertEqual(response.data, serializer.data)


class TestGetFilteredProjectsList(TestCase):
    url = BASE_URL + "get-filtered-projects-list"

    def test_req(self):
        response = client.get(self.url + "?categories=&markets=")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_res(self):
        categories = Project.get_project_categories_choices(index=0)
        category01 = categories[0]
        category02 = categories[1]

        market01 = Market.objects.create(name="Innovation")
        market02 = Market.objects.create(name="Finance")
        market03 = Market.objects.create(name="Beverages")

        project01 = Project.objects.create(category=category01)
        project01.markets.add(market01)
        project01.save()

        project02 = Project.objects.create(category=category01)
        project02.markets.add(market02)
        project02.save()

        project03 = Project.objects.create(category=category02)
        project03.markets.add(market03)
        project03.save()

        project04 = Project.objects.create(category=category02)
        project04.markets.add(market01, market02)
        project04.save()

        # should return all projects
        response = client.get(
            self.url + f"?categories={category01};{category02}&markets={market01.name};{market02.name};{market03.name}"
        )
        self.assertEqual(response.data, ProjectSerializer01(Project.objects.all(), many=True).data)

        # should return only projects 03 and 04
        response = client.get(
            self.url + f"?categories={category02}&markets={market01.name}; {market02.name};{market03.name}"
        )
        self.assertEqual(response.data, ProjectSerializer01([project03, project04], many=True).data)

        # shouldn't return any project
        response = client.get(self.url + f"?categories={category01};{category02}&markets=")
        self.assertEqual(response.data, ProjectSerializer01([], many=True).data)

        # shouldn't return any project
        response = client.get(self.url + f"?categories=&markets={market01.name};{market02.name};{market03.name}")
        self.assertEqual(response.data, ProjectSerializer01([], many=True).data)


class TestGetProjectsCategoriesList(TestCase):
    url = BASE_URL + "get-projects-categories-list"

    def test_req(self):
        response = client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_res(self):
        categories = [
            {"value": category[0], "readable": category[1]} for category in Project.get_project_categories_choices()
        ]
        response = client.get(self.url)

        self.assertEqual(response.data, categories)


class TestCreateProject(TestCase):
    pass


class TestGetProject(TestCase):
    url = BASE_URL + "get-project/"

    def test_req(self):
        response = client.get(f"{self.url}1")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        Project.objects.create()

        response = client.get(f"{self.url}1")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_res(self):
        response = client.get(f"{self.url}1")
        self.assertEqual(response.data, "Projeto não encontrado")

        project = Project.objects.create()

        response = client.get(f"{self.url}1")
        self.assertEqual(response.data, ProjectSerializer02(project).data)


class TestEditProject(TestCase):
    pass


class TestInviteUsersToProject(TestCase):
    pass


class TestUninviteUserFromProject(TestCase):
    pass


class TestAskToJoinProject(TestCase):
    pass


class TestRemoveUserFromProject(TestCase):
    pass


class TestReplyProjectInvitation(TestCase):
    pass


class TestReplyProjectEnteringRequest(TestCase):
    pass


class TestEditProjectDescription(TestCase):
    pass


class TestCreateLink(TestCase):
    pass


class TestDeleteLink(TestCase):
    pass
