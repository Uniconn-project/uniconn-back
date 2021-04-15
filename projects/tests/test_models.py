import datetime

import pytz
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from django.test import TestCase
from profiles.models import Mentor, Profile, Student
from universities.models import MajorField, University


class TestProjects(TestCase):
    """
    Eu suponho que como no arquivo __ini__.pyi tem apenas a definição de pegar o model do user
    e vendo o diagrama posso inferir que a tabela projects tem a relação com a tabela students
    que por sua vez tem relação com a profile que por ultimo se relaciona com user.
    Ontem falamos sobre o tal efeito cascata então suponho que se eu pego um modelo de user por
    conseguinte estarei testando usando a tabela students dentro do projects.
    Posso estar equivocado, devo declarar um getter pra pegar um student model no __init__.pyi?
    """

    def setUp(self):
        self.User = get_user_model()
