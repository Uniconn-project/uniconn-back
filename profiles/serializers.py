from django.contrib.auth import get_user_model
from rest_framework import serializers
from universities.serializers import MajorSerializer01, UniversitySerializer01

from .models import Link, Profile, Skill

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email"]


class SkillSerializer01(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ["id", "name"]


class LinkSerializer01(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = ["id", "name", "href"]


class ProfileSerializer01(serializers.ModelSerializer):
    """
    Heavy Profile serializer - useful for profile pages
    """

    user = UserSerializer()
    skills = SkillSerializer01(many=True)
    links = LinkSerializer01(many=True)
    university = UniversitySerializer01()
    major = MajorSerializer01()

    class Meta:
        model = Profile
        fields = [
            "id",
            "user",
            "photo",
            "first_name",
            "last_name",
            "bio",
            "birth_date",
            "skills",
            "links",
            "is_attending_university",
            "university",
            "major",
            "created_at",
        ]


class ProfileSerializer02(serializers.ModelSerializer):
    """
    Lightest Profile serializer - only id, user and image
    """

    user = UserSerializer()

    class Meta:
        model = Profile
        fields = ["id", "user", "photo"]


class ProfileSerializer03(serializers.ModelSerializer):
    """
    Light Profile serializer - useful for profile list items
    """

    user = UserSerializer()

    class Meta:
        model = Profile
        fields = [
            "id",
            "user",
            "photo",
            "first_name",
            "last_name",
            "bio",
        ]
