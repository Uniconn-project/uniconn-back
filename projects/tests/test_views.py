from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from profiles.models import Mentor, Student
from profiles.tests.test_views import User
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

        for method in ["delete", "put", "patch", "post"]:
            response = getattr(client, method)(self.url)
            self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

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

        for method in ["delete", "put", "patch", "post"]:
            response = getattr(client, method)(self.url)
            self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_res(self):
        project01 = Project.objects.create()
        project02 = Project.objects.create()

        serializer = ProjectSerializer01([project02, project01], many=True)

        response = client.get(self.url)
        self.assertEqual(response.data, serializer.data)


class TestGetFilteredProjectsList(TestCase):
    url = BASE_URL + "get-filtered-projects-list"

    def test_req(self):
        response = client.get(self.url + "?categories=&markets=")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        for method in ["delete", "put", "patch", "post"]:
            response = getattr(client, method)(self.url)
            self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

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
        self.assertEqual(response.data, ProjectSerializer01([project04, project03], many=True).data)

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

        for method in ["delete", "put", "patch", "post"]:
            response = getattr(client, method)(self.url)
            self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_res(self):
        categories = [
            {"value": category[0], "readable": category[1]} for category in Project.get_project_categories_choices()
        ]
        response = client.get(self.url)

        self.assertEqual(response.data, categories)


class TestCreateProject(TestCase):
    url = BASE_URL + "create-project"

    def test_req(self):
        response = client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        for method in ["get", "delete", "put", "patch"]:
            response = getattr(client, method)(self.url)
            self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_res(self):
        profile = User.objects.create().profile
        mentor = Mentor.objects.create(profile=profile)
        client.force_login(profile.user)

        response = client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, "Somente universitários podem criar projetos!")

        mentor.delete()
        Student.objects.create(profile=profile)

        response = client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, "Dados inválidos!")

        market01 = Market.objects.create(name="energy")
        market02 = Market.objects.create(name="tech")

        request_data = {
            "category": "startup",
            "name": "4Share",
            "slogan": "Providing energy for the future",
            "markets": ["tech", "energy"],
        }

        response = client.post(self.url, {**request_data, "name": ""}, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, "Todos os campos devem ser preenchidos!")

        response = client.post(self.url, {**request_data, "slogan": ""}, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, "Todos os campos devem ser preenchidos!")

        response = client.post(self.url, {**request_data, "name": "a" * 51}, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, "Respeite os limites de caracteres de cada campo!")

        response = client.post(self.url, {**request_data, "slogan": "a" * 126}, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, "Respeite os limites de caracteres de cada campo!")

        response = client.post(
            self.url, {**request_data, "markets": ["unexistent market"]}, content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, "Selecione pelo menos um mercado válido!")

        response = client.post(
            self.url, {**request_data, "category": "state company"}, content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, "Categoria do projeto inválida!")

        response = client.post(self.url, request_data, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, "success")

        project = Project.objects.first()

        self.assertEqual(len(Project.objects.all()), 1)
        self.assertEqual(project.category, request_data["category"])
        self.assertEqual(project.name, request_data["name"])
        self.assertEqual(project.slogan, request_data["slogan"])
        self.assertEqual(list(project.markets.all()), [market01, market02])


class TestGetProject(TestCase):
    url = BASE_URL + "get-project/"

    def test_req(self):
        response = client.get(f"{self.url}1")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        Project.objects.create()

        response = client.get(f"{self.url}1")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        for method in ["delete", "put", "patch", "post"]:
            response = getattr(client, method)(f"{self.url}1")
            self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_res(self):
        response = client.get(f"{self.url}1")
        self.assertEqual(response.data, "Projeto não encontrado")

        project = Project.objects.create()

        response = client.get(f"{self.url}1")
        self.assertEqual(response.data, ProjectSerializer02(project).data)


class TestEditProject(TestCase):
    url = BASE_URL + "edit-project/"

    def test_req(self):
        response = client.put(f"{self.url}1")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        for method in ["get", "delete", "post", "patch"]:
            response = getattr(client, method)(f"{self.url}1")
            self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_res(self):
        profile = User.objects.create().profile
        mentor = Mentor.objects.create(profile=profile)
        client.force_login(profile.user)

        response = client.put(f"{self.url}1")
        self.assertEqual(response.data, "Projeto não encontrado")

        project = Project.objects.create()
        project.mentors.add(mentor)
        project.save()

        response = client.put(f"{self.url}1")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, "Somente universitários podem editar o projeto!")

        mentor.delete()
        student = Student.objects.create(profile=profile)

        response = client.put(f"{self.url}1")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, "Você não faz parte do projeto!")

        project.students.add(student)
        project.save()

        response = client.put(f"{self.url}1")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, "Dados inválidos!")

        market01 = Market.objects.create(name="energy")
        market02 = Market.objects.create(name="tech")

        request_data = {
            "image": None,
            "name": "4Share",
            "category": "startup",
            "slogan": "Providing energy for the future",
            "markets": ["tech", "energy"],
        }

        response = client.put(f"{self.url}1", {**request_data, "name": "a" * 51}, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, "Respeite os limites de caracteres de cada campo!")

        response = client.put(f"{self.url}1", {**request_data, "slogan": "a" * 126}, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, "Respeite os limites de caracteres de cada campo!")

        response = client.put(
            f"{self.url}1", {**request_data, "category": "state company"}, content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, "Categoria do projeto inválida!")

        response = client.put(f"{self.url}1", request_data, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, "success")

        project.refresh_from_db()

        self.assertEqual(project.image, "default_project.jpg")
        self.assertEqual(project.name, request_data["name"])
        self.assertEqual(project.category, request_data["category"])
        self.assertEqual(project.slogan, request_data["slogan"])
        self.assertEqual(list(project.markets.all()), [market01, market02])

        # TODO project image upload test


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
