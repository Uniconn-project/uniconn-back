from django.contrib.auth.models import User
from django.db import models
from universities.models import Major, University


class Student(models.Model):
    """
    Student table
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="student")
    photo = models.ImageField(default="profile_avatar.jpg", upload_to="profile_photos")
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    university = models.ForeignKey(
        University, on_delete=models.SET_NULL, related_name="students", blank=True, null=True
    )
    major = models.ForeignKey(Major, on_delete=models.SET_NULL, related_name="students", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering: ["-created_at"]

    def __str__(self):
        return self.user.username
