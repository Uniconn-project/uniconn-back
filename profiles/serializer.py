from django.contrib.auth import get_user_model
from projects.serializers import MarketSerializer01
from rest_framework import serializers
from universities.serializers import MajorSerializer01, UniversitySerializer01

from .models import Mentor, Profile, Student

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]


class ProfileSerializer01(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = ["id", "user", "photo", "first_name", "last_name", "birth_date", "created_at"]


class StudentSerializer01(serializers.ModelSerializer):
    profile = ProfileSerializer01()
    university = UniversitySerializer01()
    major = MajorSerializer01()

    class Meta:
        model = Student
        fields = ["id", "profile", "university", "major"]


class MentorSerializer01(serializers.ModelSerializer):
    profile = ProfileSerializer01()
    markets = MarketSerializer01()

    class Meta:
        model = Student
        fields = ["id", "profile", "markets"]
