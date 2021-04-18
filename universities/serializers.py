from rest_framework import serializers

from .models import Major, University


class UniversitySerializer01(serializers.ModelSerializer):
    """
    University serializer that serializes only the *id* and *name* of a given university object.
    """

    class Meta:
        model = University
        fields = ["id", "name"]


class MajorSerializer01(serializers.ModelSerializer):
    """
    Major serializer that serializes only the *id* and *name* of a given major object.
    """

    class Meta:
        model = Major
        fields = ["id", "name"]
