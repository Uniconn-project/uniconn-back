from django.db import models
from django.utils.translation import gettext_lazy as _
from profiles.models import Mentor, Student
from universities.models import MajorField


class Project(models.Model):
    """
    Project table
    """

    project_categories_choices = [
        ("startup", _("startup")),
        ("junior_enterprise", _("junior enterprise")),
        ("academic", _("academic project")),
    ]

    category = models.CharField(max_length=50, choices=project_categories_choices)
    name = models.CharField(max_length=50, blank=True, null=True)
    description = models.CharField(max_length=300, blank=True, null=True)
    students = models.ManyToManyField(Student, related_name="projects")
    mentors = models.ManyToManyField(Mentor, related_name="projects")
    fields = models.ManyToManyField(MajorField, related_name="projects")
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name
