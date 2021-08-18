from profiles.serializers import ProfileSerializer03
from rest_framework import serializers

from .models import Chat


class ChatSerializer01(serializers.ModelSerializer):
    members = ProfileSerializer03(many=True)

    class Meta:
        model = Chat
        fields = ["id", "members"]
