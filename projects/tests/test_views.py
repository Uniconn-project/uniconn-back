from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from profiles.models import Mentor, Student
from rest_framework import status

from ..models import (
    Discussion,
    DiscussionReply,
    DiscussionStar,
    Link,
    Market,
    Project,
    ProjectStar,
)
from ..serializers import MarketSerializer01, ProjectSerializer01, ProjectSerializer02

User = get_user_model()
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
        market01 = Market.objects.create(name="beverages")
        market02 = Market.objects.create(name="genetical engineering")

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

        link01 = Link.objects.create()
        link02 = Link.objects.create()
        link03 = Link.objects.create()

        tool01 = Link.objects.create()
        tool02 = Link.objects.create()
        tool03 = Link.objects.create()

        project.links.add(tool01, tool02, tool03)
        project.links.add(link01, link02, link03)
        project.save()

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
    url = BASE_URL + "invite-{}-to-project/{}"

    def test_req(self):
        response = client.put(self.url.format("students", "1"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        for method in ["get", "delete", "post", "patch"]:
            response = getattr(client, method)(self.url.format("students", "1"))
            self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_res(self):
        profile = User.objects.create().profile
        mentor = Mentor.objects.create(profile=profile)
        client.force_login(profile.user)

        project = Project.objects.create()
        project.mentors.add(mentor)

        response = client.put(self.url.format("students", "1"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, "Somente universitários podem convidar usuários para o projeto!")

        mentor.delete()
        student = Student.objects.create(profile=profile)

        response = client.put(self.url.format("students", "2"))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, "Projeto não encontrado!")

        response = client.put(self.url.format("students", "1"))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, "Dados inválidos!")

        request_data = {"students": []}

        response = client.put(self.url.format("students", "1"), request_data, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, "Você não faz parte do projeto!")

        project.students.add(student)

        response = client.put(self.url.format("invalid type", "1"), request_data, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, "Dados inválidos!")

        response = client.put(self.url.format("students", "1"), request_data, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, "Nenhum universitário foi encontrado!")

        response = client.put(self.url.format("mentors", "1"), {"mentors": []}, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, "Nenhum mentor foi encontrado!")

        student01 = Student.objects.create(profile=User.objects.create(username="austin").profile)
        student02 = Student.objects.create(profile=User.objects.create(username="justin").profile)
        mentor01 = Mentor.objects.create(profile=User.objects.create(username="peter").profile)
        mentor02 = Mentor.objects.create(profile=User.objects.create(username="carol").profile)

        response = client.put(
            self.url.format("students", "1"),
            {"students": [student01.profile.user.username, student02.profile.user.username]},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, "success")

        self.assertEqual(list(project.pending_invited_students.all()), [student02, student01])

        response = client.put(
            self.url.format("mentors", "1"),
            {"mentors": [mentor01.profile.user.username, mentor02.profile.user.username]},
            content_type="application/json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, "success")

        self.assertEqual(list(project.pending_invited_mentors.all()), [mentor02, mentor01])


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


class TestStarProject(TestCase):
    url = BASE_URL + "star-project/"

    def test_req(self):
        response = client.post(f"{self.url}1")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        for method in ["get", "delete", "put", "patch"]:
            response = getattr(client, method)(f"{self.url}1")
            self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_res(self):
        user = User.objects.create(username="mosh")
        client.force_login(user)

        response = client.post(f"{self.url}1")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, "Projeto não encontrado!")

        project = Project.objects.create()

        self.assertFalse(ProjectStar.objects.exists())

        response = client.post(f"{self.url}1")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, "success")

        self.assertEqual(len(ProjectStar.objects.all()), 1)
        self.assertTrue(ProjectStar.objects.filter(profile=user.profile, project=project).exists())

        response = client.post(f"{self.url}1")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, "Você não pode curtir o mesmo projeto mais de uma vez!")


class TestUnstarProject(TestCase):
    url = BASE_URL + "unstar-project/"

    def test_req(self):
        response = client.delete(f"{self.url}1")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        for method in ["get", "post", "put", "patch"]:
            response = getattr(client, method)(f"{self.url}1")
            self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_res(self):
        user = User.objects.create(username="mosh")
        client.force_login(user)

        response = client.delete(f"{self.url}1")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, "Projeto não encontrado!")

        project = Project.objects.create()

        response = client.delete(f"{self.url}1")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, "Curtida não encontrada!")

        star = ProjectStar.objects.create(project=project)
        # asserting the view will only delete a project's star if it was created by the request user
        response = client.delete(f"{self.url}1")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, "Curtida não encontrada!")
        star.delete()

        ProjectStar.objects.create(profile=user.profile, project=project)

        response = client.delete(f"{self.url}1")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, "success")

        self.assertFalse(ProjectStar.objects.exists())


class TestLeaveProject(TestCase):
    url = BASE_URL + "leave-project/"

    def test_req(self):
        response = client.patch(f"{self.url}1")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        for method in ["get", "post", "put", "delete"]:
            response = getattr(client, method)(f"{self.url}1")
            self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_res(self):
        user = User.objects.create(username="mosh")
        client.force_login(user)

        response = client.patch(f"{self.url}1")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, "Projeto não encontrado!")

        project = Project.objects.create()

        response = client.patch(f"{self.url}1")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, "Você não faz parte do projeto!")

        student = Student.objects.create(profile=user.profile)
        project.students.add(student)
        project.save()

        self.assertIn(student, project.students.all())
        response = client.patch(f"{self.url}1")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, "success")
        self.assertNotIn(student, project.students.all())

        student.delete()

        mentor = Mentor.objects.create(profile=user.profile)
        project.mentors.add(mentor)
        project.save()

        self.assertIn(mentor, project.mentors.all())
        response = client.patch(f"{self.url}1")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, "success")
        self.assertNotIn(mentor, project.mentors.all())


class TestCreateLink(TestCase):
    pass


class TestDeleteLink(TestCase):
    pass


class TestCreateTool(TestCase):
    pass


class TestDeleteTool(TestCase):
    pass


class TestCreateProjectDiscussion(TestCase):
    pass


class TestGetProjectDiscussions(TestCase):
    pass


class TestGetProjectDiscussion(TestCase):
    pass


class TestDeleteProjectDiscussion(TestCase):
    pass


class TestStarDiscussion(TestCase):
    url = BASE_URL + "star-discussion/"

    def test_req(self):
        response = client.post(f"{self.url}1")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        for method in ["get", "delete", "put", "patch"]:
            response = getattr(client, method)(f"{self.url}1")
            self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_res(self):
        user = User.objects.create(username="mosh")
        client.force_login(user)

        response = client.post(f"{self.url}1")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, "Discussão não encontrada!")

        discussion = Discussion.objects.create()

        self.assertFalse(DiscussionStar.objects.exists())

        response = client.post(f"{self.url}1")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, "success")

        self.assertEqual(len(DiscussionStar.objects.all()), 1)
        self.assertTrue(DiscussionStar.objects.filter(profile=user.profile, discussion=discussion).exists())

        response = client.post(f"{self.url}1")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, "Você não pode curtir a mesma discussão mais de uma vez!")


class TestUnstarDiscussion(TestCase):
    url = BASE_URL + "unstar-discussion/"

    def test_req(self):
        response = client.delete(f"{self.url}1")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        for method in ["get", "post", "put", "patch"]:
            response = getattr(client, method)(f"{self.url}1")
            self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_res(self):
        user = User.objects.create(username="mosh")
        client.force_login(user)

        response = client.delete(f"{self.url}1")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, "Discussão não encontrada!")

        discussion = Discussion.objects.create()

        response = client.delete(f"{self.url}1")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, "Curtida não encontrada!")

        star = DiscussionStar.objects.create(discussion=discussion)
        # asserting the view will only delete a discussion's star if it was created by the request user
        response = client.delete(f"{self.url}1")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, "Curtida não encontrada!")
        star.delete()

        DiscussionStar.objects.create(profile=user.profile, discussion=discussion)

        response = client.delete(f"{self.url}1")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, "success")

        self.assertFalse(DiscussionStar.objects.exists())


class TestReplyDiscussion(TestCase):
    url = BASE_URL + "reply-discussion/"

    def test_req(self):
        response = client.post(f"{self.url}1")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        for method in ["get", "delete", "put", "patch"]:
            response = getattr(client, method)(f"{self.url}1")
            self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_res(self):
        user = User.objects.create(username="mosh")
        client.force_login(user)

        response = client.post(f"{self.url}1")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, "Dados inválidos!")

        post_data = {"content": "Lorem ipsum dolor sit amet"}

        response = client.post(f"{self.url}1", post_data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, "Discussão não encontrada!")

        discussion = Discussion.objects.create()

        response = client.post(f"{self.url}1", {**post_data, "content": "aa"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, "O comentário não pode ter menos de 3 caracteres!")

        response = client.post(f"{self.url}1", {**post_data, "content": "a" * 301})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, "Respeite o limite de caracteres!")

        self.assertFalse(DiscussionReply.objects.exists())

        response = client.post(f"{self.url}1", post_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, "success")

        self.assertEqual(len(DiscussionReply.objects.all()), 1)
        self.assertTrue(
            DiscussionReply.objects.filter(profile=user.profile, discussion=discussion, content=post_data["content"])
        )


class TestDeleteDiscussionReply(TestCase):
    url = BASE_URL + "delete-discussion-reply/"

    def test_req(self):
        response = client.delete(f"{self.url}1")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        for method in ["get", "put", "patch", "post"]:
            response = getattr(client, method)(f"{self.url}1")
            self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_res(self):
        user = User.objects.create()
        client.force_login(user)

        response = client.delete(f"{self.url}1")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, "Comentário não encontrado!")

        reply = DiscussionReply.objects.create()

        response = client.delete(f"{self.url}1")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, "O comentário não é seu!")

        reply.profile = user.profile
        reply.save()

        self.assertTrue(DiscussionReply.objects.exists())

        response = client.delete(f"{self.url}1")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, "success")

        self.assertFalse(DiscussionReply.objects.exists())
