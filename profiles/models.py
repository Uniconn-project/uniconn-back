from django.contrib.auth.models import AbstractUser
from django.db import models
from universities.models import Major, University


class User(AbstractUser):
    """
    Custom user model - only used for authentication
    Even we don't needing a custom user model now, it's bad practice to use the default django model
    since we wouldn't be able to add custom functionality to it in the future. With that in mind,
    it's a good aproach to use a custom user model that is a copy of the django default user model, so that's what
    we're doing [=
    """

    pass


class Skill(models.Model):
    "Skill table - represents skills (e.g. programming, design, marketing)"

    name = models.CharField(max_length=50, default="", unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        super().save(*args, **kwargs)


class Profile(models.Model):
    """
    Profile table - all users of the platform (students, mentors, etc) are in this table
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    photo = models.ImageField(default="profile_avatar.jpeg", upload_to="profile_photos", blank=True, null=True)
    first_name = models.CharField(max_length=30, default="")
    last_name = models.CharField(max_length=30, default="")
    bio = models.CharField(max_length=150, default="Sem bio...")
    birth_date = models.DateField(blank=True, null=True)
    linkedIn = models.CharField(max_length=50, default="")
    skills = models.ManyToManyField(Skill, related_name="profiles", blank=True)
    is_attending_university = models.BooleanField(blank=True, null=True)
    university = models.ForeignKey(
        University, on_delete=models.SET_NULL, related_name="profiles", blank=True, null=True
    )
    major = models.ForeignKey(Major, on_delete=models.SET_NULL, related_name="profiles", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

    @property
    def projects(self):
        return [membership.project for membership in self.project_memberships.all()]
