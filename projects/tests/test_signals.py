from unittest import signals

from django.test import TestCase

from ..models import Project, ToolCategory


class TestSignals(TestCase):
    def setUp(self):
        pass

    def test_create_tools_categories_signal(self):
        project = Project.objects.create()

        self.assertEqual(len(project.tools_categories.all()), 3)
        self.assertTrue(ToolCategory.objects.filter(name="Gerenciadores de Tarefas", project=project).exists())
        self.assertTrue(ToolCategory.objects.filter(name="Documentos em Nuvem", project=project).exists())
        self.assertTrue(ToolCategory.objects.filter(name="Ferramentas de Desenvolvimento", project=project).exists())
