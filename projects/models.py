from django.db import models
from profiles.models import Mentor, Student


class Market(models.Model):
    """
    Market table - used to connect mentors to projects related to their markets
    """

    name = models.CharField(max_length=50, blank=True, null=True, unique=True)
    mentors = models.ManyToManyField(Mentor, related_name="markets", blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.name is not None:
            self.name = self.name.lower()

        super().save(*args, **kwargs)


project_categories_choices = [
    ("startup", "startup"),
    ("junior_enterprise", "empresa júnior"),
    ("academic", "projeto acadêmico"),
    ("social_project", "projeto social"),
]


class Project(models.Model):
    """
    Project table
    """

    category = models.CharField(max_length=50, choices=project_categories_choices)
    name = models.CharField(max_length=50, blank=True, null=True)
    slogan = models.CharField(help_text="Very quick description", max_length=100, blank=True, null=True)
    description = models.CharField(help_text="Detailed description", max_length=1000, blank=True, null=True)
    image = models.ImageField(default="default_project.jpg", upload_to="projects_photos")
    students = models.ManyToManyField(Student, related_name="projects", blank=True)
    mentors = models.ManyToManyField(Mentor, related_name="projects", blank=True)
    markets = models.ManyToManyField(Market, related_name="projects")
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    @staticmethod
    def get_project_categories_choices(index=1):
        return [project_category[index] for project_category in project_categories_choices]

    @staticmethod
    def get_project_categories_values_from_readable(readable_categories):
        return [
            project_category[0]
            for project_category in project_categories_choices
            if project_category[1] in readable_categories
        ]

    def __str__(self):
        return self.name if self.name is not None else ""

    @property
    def students_profile(self):
        return [student.profile for student in self.students.all()]

    @property
    def mentors_profile(self):
        return [mentor.profile for mentor in self.mentors.all()]
