from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.fields import related
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


class StudentSkill(models.Model):
    "Student skill table - represents students skills (e.g. programming, design, marketing)"

    name = models.CharField(max_length=50, default="", unique=True)

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
    linkedIn = models.CharField(max_length=50, default="")
    birth_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

    @property
    def type(self):
        if hasattr(self, "student"):
            return "student"
        elif hasattr(self, "mentor"):
            return "mentor"


class Student(models.Model):
    """
    Student table
    """

    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name="student")
    university = models.ForeignKey(
        University, on_delete=models.SET_NULL, related_name="students", blank=True, null=True
    )
    major = models.ForeignKey(Major, on_delete=models.SET_NULL, related_name="students", blank=True, null=True)

    skills = models.ManyToManyField(StudentSkill, related_name="students", blank=True)

    class Meta:
        ordering = ["-profile__id"]

    def __str__(self):
        return f"{self.profile.user.username} [STUDENT]"


class Mentor(models.Model):
    """
    Mentor table
    """

    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name="mentor", blank=True, null=True)

    class Meta:
        ordering = ["-profile__id"]

    def __str__(self):
        return f"{self.profile.user.username} [MENTOR]"
