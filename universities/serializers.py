from rest_framework import serializers

from .models import University


class UniversitySerializer01(serializers.ModelSerializer):
    """
    University serializer that serializes only the *id* and *name* of a given university object.
    """

    class Meta:
        model = University
        fields = ["id", "name"]
