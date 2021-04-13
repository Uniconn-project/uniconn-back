from django.contrib.auth.models import AbstractUser
from django.db import models
from universities.models import Major, University


class User(AbstractUser):
    pass


class Profile(models.Model):
    """
    Profile table - all users of the platform (students, mentors, etc) are in this table
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    photo = models.ImageField(default="profile_avatar.jpg", upload_to="profile_photos")
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)


class Student(models.Model):
    """
    Student table
    """

    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name="student")
    university = models.ForeignKey(
        University, on_delete=models.SET_NULL, related_name="students", blank=True, null=True
    )
    major = models.ForeignKey(Major, on_delete=models.SET_NULL, related_name="students", blank=True, null=True)

    class Meta:
        ordering: ["-created_at"]

    def __str__(self):
        return self.user.username


class Mentor(models.Model):
    """
    Mentor table
    """

    pass
