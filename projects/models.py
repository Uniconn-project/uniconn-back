from django.db import models
from profiles.models import Mentor, Student


class Market(models.Model):
    """
    Market table - relates with mentors and projects
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


class Link(models.Model):
    """
    Link table
    """

    name = models.CharField(max_length=50, blank=True, null=True)
    href = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self):
        return self.name


class Project(models.Model):
    """
    Project table
    """

    category = models.CharField(max_length=50, choices=project_categories_choices)
    name = models.CharField(max_length=50, blank=True, null=True)
    slogan = models.CharField(help_text="Very quick description", max_length=100, blank=True, null=True)
    description = models.CharField(
        help_text="Detailed description",
        default='{"blocks": [{"key": "5v3ub", "text": "Sem descrição...", "type": "unstyled", "depth": 0, "inlineStyleRanges": [], "entityRanges": [], "data": {}}], "entityMap": {}}',
        max_length=1000,
    )
    image = models.ImageField(default="default_project.jpg", upload_to="projects_photos")
    students = models.ManyToManyField(Student, related_name="projects", blank=True)
    mentors = models.ManyToManyField(Mentor, related_name="projects", blank=True)
    pending_invited_students = models.ManyToManyField(Student, related_name="pending_projects_invitations", blank=True)
    pending_invited_mentors = models.ManyToManyField(Mentor, related_name="pending_projects_invitations", blank=True)
    markets = models.ManyToManyField(Market, related_name="projects")
    links = models.ManyToManyField(Link, related_name="projects", blank=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    @staticmethod
    def get_project_categories_choices(index=-1):
        return [
            (project_category[index] if index != -1 else project_category)
            for project_category in project_categories_choices
        ]

    def __str__(self):
        return self.name if self.name is not None else ""

    @property
    def category_value_and_readable(self):
        return {"value": self.category, "readable": self.get_category_display()}

    @property
    def students_profile(self):
        return [student.profile for student in self.students.all()]

    @property
    def mentors_profile(self):
        return [mentor.profile for mentor in self.mentors.all()]

    @property
    def pending_invited_students_profile(self):
        return [student.profile for student in self.pending_invited_students.all()]

    @property
    def pending_invited_mentors_profile(self):
        return [mentor.profile for mentor in self.pending_invited_mentors.all()]
