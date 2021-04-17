import datetime

import pytz
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from django.test import TestCase

# Importar de onde a tabela é criada.
from profiles.models import Mentor, Profile, Student
from projects.models import Market, Project

## Students, Markets, impotar esses dois e criar instacias e adiciona istacia do projects
## Importar o model do arquivo que ele foi criado

# Create user in test
# user = self.User.objects.create(username=username, password="secret")

# O model é uma classe por isso letra maiscula, recebe o model
User = get_user_model()


class TestProjects(TestCase):
    # Test instance of Project class (table)
    """
    Meu raciocínio aqui é que eu devo pelo menos preecher o instaciamento da tabela projects
    que é a primeira que eu quero testar, perguntar pro Felipe se preencher os parâmetros do
    construtor da mesma é algo válido ou se já existe uma abstração para isso.
    """

    # Nome padrão da função/ Convenção
    def test_model(self):
        # Variáveis de tempo
        now_naive = datetime.datetime.now()
        timezone = pytz.timezone("UTC")
        now_aware = timezone.localize(now_naive)

        # test create
        project = Project.objects.create()
        self.assertIsInstance(project, Project)
        # Já que o id que é primary key é auto incremental e começa com 1, testando se ele existe
        self.assertEqual(project.pk, 1)
        self.assertLessEqual(now_aware, project.created_at)
        self.assertLessEqual(now_aware, project.updated_at)

        # test edit
        category = "Startup"
        description = "Innovating the world"
        name = "Connecticonn"

        # Sempre que um usuário for criado um profile já é feito, Felipe's magic
        # Os que precisarem de objetos para ser criados, deixar junto
        user01 = User.objects.create(username="DjagoPreso")
        user02 = User.objects.create(username="DjangoLivre")
        profile01 = user01.profile
        profile02 = user02.profile

        # adding the students to project
        student01 = Student.objects.create(profile=profile01)
        student02 = Student.objects.create(profile=profile02)
        project.students.add(student01, student02)

        # Testing mentors
        # creating users in order to create profile
        user03 = User.objects.create(username="Mentor1")
        user04 = User.objects.create(username="Mentor2")
        profile03 = user03.profile
        profile04 = user04.profile

        # creating mentors
        mentor01 = Mentor.objects.create(profile=profile03)
        mentor02 = Mentor.objects.create(profile=profile04)
        project.mentors.add(mentor01, mentor02)

        # testing markets
        # Já que estou testando o campo project não precisa inicializar os parâmetros do construtor do Market
        # Quando a relação é 1 to 1, tem que inciliazar e passar o arg.
        market01 = Market.objects.create()
        market02 = Market.objects.create()
        project.markets.add(market01, market02)
        # Este salva tudo pra cima, não precisa repetir

        project.name = name
        project.description = description
        project.category = category
        # Desta linha pra cima primeiro inicializei os objetos, e depois editei os mesmos
        project.save()

        # Testando se o que eu inicializei, se a propriedade do objeto foi editada
        self.assertEqual(project.name, name)
        self.assertEqual(project.description, description)
        self.assertEqual(project.category, category)

        # Testando os objetos
        # O método .all() retorna uma lista
        # Testando se a largura do array e igual, ao parâmetro desejado
        students = project.students.all()
        self.assertEqual(len(students), 2)

        # Garantido se eles estão de fato na lista
        self.assertIn(student01, students)
        self.assertIn(student02, students)

        # Mesma rotina de cima
        mentors = project.mentors.all()
        self.assertEqual(len(mentors), 2)
        self.assertIn(mentor01, mentors)
        self.assertIn(mentor02, mentors)

        markets = project.markets.all()
        self.assertEqual(len(markets), 2)
        self.assertIn(market01, markets)
        self.assertIn(market02, markets)

        # A partir daqui de cima, testamos criar e editar

        # test delete
        project.delete()
        self.assertFalse(Project.objects.filter().exists())

    def test_related_name(self):
        # Isso só acontece pra tabelas, RELACIONAL
        project = Project.objects.create()
        user01 = User.objects.create(username="RobsonFaixaPreta")
        student = Student.objects.create(profile=user01.profile)
        project.students.add(student)

        # Testing related name if project is instance of students
        # Basically is testing if it's possible to acess student.projects and acess all projects
        # Se a partir de estudents eu consigo acessar projects por meio students.projects
        # Que é o related name definido no model.py que é a declaração do model
        self.assertIn(project, student.projects.all())

        # Test mentors two way
        user02 = User.objects.create(username="DjaguinhoDoQuero")
        mentor = Mentor.objects.create(profile=user02.profile)
        project.mentors.add(mentor)
        self.assertIn(project, mentor.projects.all())

        # Same for market
        market = Market.objects.create()
        project.markets.add(market)
        self.assertIn(project, market.projects.all())

    def test_str(self):
        project = Project.objects.create(name="UniconnForLife")
        self.assertEqual(str(project), project.name)


class TestMarket(TestCase):
    def test_model(self):
        # test create
        market = Market.objects.create()
        self.assertIsInstance(market, Market)
        self.assertEqual(market.pk, 1)

        # test edit
        user01 = User.objects.create(username="RonaldinDasQuebrada")
        profile01 = user01.profile
        mentor01 = Mentor.objects.create(profile=profile01)

        user02 = User.objects.create()
        profile02 = user02.profile
        mentor02 = Mentor.objects.create(profile=profile02)

        market.mentors.add(mentor01, mentor02)

        name = "DrugMarket"
        market.name = name

        market.save()

        self.assertEqual(market.name, name.lower())
        self.assertEqual(len(market.mentors.all()), 2)
        self.assertIn(mentor01, market.mentors.all())
        self.assertIn(mentor02, market.mentors.all())

        # test delete
        self.assertIsInstance(market, Market)
        market.delete()
        self.assertFalse(Market.objects.filter().exists())

    def test_related_name(self):
        # Já que é uma relação um teste. MANY TO MANY
        user = User.objects.create(username="JuninDaEsquina")
        mentor = Mentor.objects.create(profile=user.profile)
        market = Market.objects.create()
        market.mentors.add(mentor)

        self.assertIn(market, mentor.markets.all())

    # Testando parada da string __str__
    def test_str(self):
        market = Market.objects.create(name="UniconnForLife")
        self.assertEqual(str(market), market.name)
