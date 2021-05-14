from profiles.serializers import ProfileSerializer01, ProfileSerializer02
from rest_framework import serializers

from .models import Market, Project


class MarketSerializer01(serializers.ModelSerializer):
    """
    Market serializer that serializes only the *id* and *name* of a given market object.
    """

    class Meta:
        model = Market
        fields = ["id", "name"]


class ProjectSerializer01(serializers.ModelSerializer):
    students = ProfileSerializer01(source="students_profile", many=True)
    mentors = ProfileSerializer02(source="mentors_profile", many=True)
    markets = MarketSerializer01(many=True)

    class Meta:
        model = Project
        fields = ["id", "category", "name", "description", "students", "mentors", "markets"]
