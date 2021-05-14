from django.contrib.auth import get_user_model
from rest_framework import serializers
from universities.serializers import MajorSerializer01, UniversitySerializer01

from .models import Mentor, Profile, Student

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]


class StudentSerializer01(serializers.ModelSerializer):
    university = UniversitySerializer01()
    major = MajorSerializer01()

    class Meta:
        model = Student
        fields = ["id", "university", "major"]


class MentorSerializer01(serializers.ModelSerializer):
    class Meta:
        model = Mentor
        fields = ["id", "markets"]


class ProfileSerializer01(serializers.ModelSerializer):
    """
    Profile serializer for student
    """

    user = UserSerializer()
    student = StudentSerializer01()

    class Meta:
        model = Profile
        fields = ["student", "user", "photo", "first_name", "last_name", "birth_date", "created_at"]


class ProfileSerializer02(serializers.ModelSerializer):
    """
    Profile serializer for mentor
    """

    user = UserSerializer()
    mentor = MentorSerializer01()

    class Meta:
        model = Profile
        fields = ["mentor", "user", "photo", "first_name", "last_name", "birth_date", "created_at"]
