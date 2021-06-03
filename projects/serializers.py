from profiles.serializers import ProfileSerializer03, ProfileSerializer03
from rest_framework import serializers

from .models import Link, Market, Project


class MarketSerializer01(serializers.ModelSerializer):
    """
    Market serializer that serializes only the *id* and *name* of a given market object.
    """

    class Meta:
        model = Market
        fields = ["id", "name"]


class LinksSerializer01(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = ["id", "name", "href"]


class ProjectSerializer01(serializers.ModelSerializer):
    students = ProfileSerializer03(source="students_profile", many=True)
    mentors = ProfileSerializer03(source="mentors_profile", many=True)
    markets = MarketSerializer01(many=True)
    links = LinksSerializer01(many=True)
    
    class Meta:
        model = Project
        fields = ["id", "category", "name", "slogan", "image", "description", "students", "mentors", "markets", "links"]
