from django.db import models
from django.db.models.aggregates import Max
from profiles.models import Mentor, Profile, Student


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

    name = models.CharField(max_length=100, blank=True, null=True)
    href = models.CharField(max_length=300, blank=True, null=True)
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Project(models.Model):
    """
    Project table
    """

    category = models.CharField(max_length=50, choices=project_categories_choices)
    name = models.CharField(max_length=50, blank=True, null=True)
    slogan = models.CharField(help_text="Very quick description", max_length=125, blank=True, null=True)
    description = models.CharField(
        help_text="Detailed description",
        default='{"blocks": [{"key": "5v3ub", "text": "Sem descrição...", "type": "unstyled", "depth": 0, "inlineStyleRanges": [], "entityRanges": [], "data": {}}], "entityMap": {}}',
        max_length=20000,
    )
    image = models.ImageField(default="default_project.jpg", upload_to="project_images")
    students = models.ManyToManyField(Student, related_name="projects", blank=True)
    mentors = models.ManyToManyField(Mentor, related_name="projects", blank=True)
    pending_invited_students = models.ManyToManyField(Student, related_name="pending_projects_invitations", blank=True)
    pending_invited_mentors = models.ManyToManyField(Mentor, related_name="pending_projects_invitations", blank=True)
    markets = models.ManyToManyField(Market, related_name="projects")
    links = models.ManyToManyField(Link, related_name="projects", blank=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-id"]

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
    def students_profiles(self):
        return [student.profile for student in self.students.all()]

    @property
    def mentors_profiles(self):
        return [mentor.profile for mentor in self.mentors.all()]

    @property
    def pending_invited_students_profiles(self):
        return [student.profile for student in self.pending_invited_students.all()]

    @property
    def pending_invited_mentors_profiles(self):
        return [mentor.profile for mentor in self.pending_invited_mentors.all()]


class ProjectEnteringRequest(models.Model):
    message = models.CharField(max_length=500, blank=True, null=True)
    project = models.ForeignKey(
        Project, related_name="entering_requests", on_delete=models.CASCADE, blank=True, null=True
    )
    profile = models.ForeignKey(
        Profile, related_name="projects_entering_requests", on_delete=models.CASCADE, blank=True, null=True
    )

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return f"{self.profile.user.username} to {self.project.name}"


discussion_categories_choices = [
    ("doubt", "dúvida"),
    ("suggestion", "sugestão"),
    ("feedback", "feedback"),
]


class Discussion(models.Model):
    title = models.CharField(max_length=125, blank=True, null=True)
    body = models.CharField(max_length=1000, blank=True, null=True)
    category = models.CharField(max_length=15, choices=discussion_categories_choices, blank=True, null=True)
    profile = models.ForeignKey(Profile, related_name="discussions", on_delete=models.CASCADE, blank=True, null=True)
    project = models.ForeignKey(Project, related_name="discussions", on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-id"]

    @staticmethod
    def get_discussion_categories_choices(index=-1):
        return [
            (discussion_category[index] if index != -1 else discussion_category)
            for discussion_category in discussion_categories_choices
        ]

    def __str__(self):
        return f"{self.profile.user.username} - {self.title}"

    @property
    def category_value_and_readable(self):
        return {"value": self.category, "readable": self.get_category_display()}


class DiscussionStar(models.Model):
    profile = models.ForeignKey(
        Profile, related_name="discussions_stars", on_delete=models.CASCADE, blank=True, null=True
    )
    discussion = models.ForeignKey(Discussion, related_name="stars", on_delete=models.CASCADE, blank=True, null=True)
    visualized = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return f"{self.profile.user.username} starred {self.discussion}"


class DiscussionReply(models.Model):
    content = models.CharField(max_length=125, blank=True, null=True)
    profile = models.ForeignKey(
        Profile, related_name="discussions_replies", on_delete=models.CASCADE, blank=True, null=True
    )
    discussion = models.ForeignKey(Discussion, related_name="replies", on_delete=models.CASCADE, blank=True, null=True)
    visualized = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return f"{self.profile.user.username} replied {self.content[:50]} to {self.discussion.title[:50]}"
