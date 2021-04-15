import datetime

import pytz
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from django.test import TestCase
from projects.models import Market, Project, Student

## Students, Markets, impotar esses dois e criar instacias e adiciona istacia do projects
## Importar o model do arquivo que ele foi criado

# Create user in test
# user = self.User.objects.create(username=username, password="secret")


class TestProjects(TestCase):
    def setUp(self):
        self.User = get_user_model()

    # Test instance of Project class (table)
    """
        Meu raciocínio aqui é que eu devo pelo menos preecher o instaciamento da tabela projects
        que é a primeira que eu quero testar, perguntar pro Felipe se preencher os parâmetros do
        construtor da mesma é algo válido ou se já existe uma abstração para isso.     
    """

    def test_model(self):
        category = "marketing"
        name = "somaSolutions"
        description = "Solutions for marketing of great enterprises"
        # Here come Students I'm must initialize a User then go to a Student instance
        username = "Jaime"
        password = "shhhh"
        self.User.objects.create(username=password, password=password)
        # Creating major
        project = Project.objects.create()
        self.assertIsInstance(project, Project)
