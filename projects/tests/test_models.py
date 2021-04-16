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
        project = Project.objects.create()
        self.assertIsInstance(project, Project)
        # Já que o id que é primary key é auto incremental e começa com 1, testando se ele existe
        self.assertEqual(project.pk, 1)

        # test edit
        category = "Startup"
        description = "Inovatint the world"
        name = "Concticonn"

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
