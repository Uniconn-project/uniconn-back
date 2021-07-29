from django.db import models
from profiles.models import Profile


class Field(models.Model):
    """
    Field table - relates with the Project table
    """

    name = models.CharField(max_length=50, blank=True, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


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

    category = models.CharField(max_length=50, choices=project_categories_choices, blank=True, null=True)
    name = models.CharField(max_length=50, blank=True)
    slogan = models.CharField(help_text="Very quick description", max_length=125, blank=True, null=True)
    description = models.CharField(
        help_text="Detailed description",
        default='{"blocks": [{"key": "5v3ub", "text": "Sem descrição...", "type": "unstyled", "depth": 0, "inlineStyleRanges": [], "entityRanges": [], "data": {}}], "entityMap": {}}',
        null=True,
        max_length=20000,
    )
    image = models.ImageField(default="default_project.jpg", upload_to="project_images")
    fields = models.ManyToManyField(Field, related_name="projects", blank=True)
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
        return self.name

    @property
    def members_profiles(self):
        return [member.profile for member in self.members.all()]

    @property
    def pending_invited_profiles(self):
        return [request.profile for request in self.requests.filter(type="invitation")]

    @property
    def category_value_and_readable(self):
        return {"value": self.category, "readable": self.get_category_display()}

    @property
    def discussions_length(self):
        return len(self.discussions.all())


project_member_role_choices = [
    ("admin", "admin"),
    ("member", "membro"),
]


class ProjectMember(models.Model):
    profile = models.ForeignKey(
        Profile, related_name="project_memberships", on_delete=models.CASCADE, blank=True, null=True
    )
    project = models.ForeignKey(Project, related_name="members", on_delete=models.CASCADE, blank=True, null=True)
    role = models.CharField(max_length=50, choices=project_member_role_choices, blank=True, null=True)

    def __str__(self):
        return f"{self.profile} [{self.role}] - {self.project}"

    @property
    def role_value_and_readable(self):
        return {"value": self.role, "readable": self.get_role_display()}


project_request_type_choices = [("invitation", "invitation"), ("entry_request", "entry_request")]


class ProjectRequest(models.Model):
    """
    Project request table
    """

    type = models.CharField(max_length=50, choices=project_request_type_choices, blank=True, null=True)
    message = models.CharField(max_length=500, blank=True)
    project = models.ForeignKey(Project, related_name="requests", on_delete=models.CASCADE, blank=True, null=True)
    profile = models.ForeignKey(
        Profile, related_name="projects_requests", on_delete=models.CASCADE, blank=True, null=True
    )

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return f"{self.project.name} [{self.type}] {self.profile.user.username}"


class Link(models.Model):
    """
    Link table
    """

    name = models.CharField(max_length=100, blank=True)
    href = models.CharField(max_length=300, blank=True)
    project = models.ForeignKey(Project, related_name="links", on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.project}"


class ToolCategory(models.Model):
    """
    Tool category table
    """

    name = models.CharField(max_length=100, blank=True)
    project = models.ForeignKey(
        Project, related_name="tools_categories", on_delete=models.CASCADE, blank=True, null=True
    )

    def __str__(self):
        return f"{self.name} - {self.project}"


class Tool(models.Model):
    """
    Tool table
    """

    category = models.ForeignKey(ToolCategory, related_name="tools", on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=100, blank=True)
    href = models.CharField(max_length=300, blank=True)

    def __str__(self):
        return self.name


class ProjectStar(models.Model):
    """
    Project star table
    """

    profile = models.ForeignKey(
        Profile, related_name="projects_stars", on_delete=models.CASCADE, blank=True, null=True
    )
    project = models.ForeignKey(Project, related_name="stars", on_delete=models.CASCADE, blank=True, null=True)
    visualized = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return f"{self.profile.user.username} starred {self.project}"


discussion_categories_choices = [
    ("doubt", "dúvida"),
    ("suggestion", "sugestão"),
    ("feedback", "feedback"),
]


class Discussion(models.Model):
    """
    Discussion table
    """

    title = models.CharField(max_length=125, blank=True)
    body = models.CharField(max_length=1000, blank=True)
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
    """
    Discussion star table
    """

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
    """
    Discussion reply table - replies are all in the same layer
    """

    content = models.CharField(max_length=300, blank=True, null=True)
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
