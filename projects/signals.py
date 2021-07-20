from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Project, ToolCategory


@receiver(post_save, sender=Project)
def post_save_create_profile(sender, instance, created, **kwargs):
    if created:
        ToolCategory.objects.create(name="Gerenciadores de Tarefas", project=instance)
        ToolCategory.objects.create(name="Documentos em Nuvem", project=instance)
        ToolCategory.objects.create(name="Ferramentas de Desenvolvimento", project=instance)
