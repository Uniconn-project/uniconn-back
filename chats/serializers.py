from profiles.serializers import ProfileSerializer02, ProfileSerializer03
from rest_framework import serializers

from .models import Chat, Message


class ChatSerializer01(serializers.ModelSerializer):
    members = ProfileSerializer03(many=True)

    class Meta:
        model = Chat
        fields = ["id", "members", "last_message"]


class MessageSerializer01(serializers.ModelSerializer):
    sender = ProfileSerializer02()
    visualized_by = ProfileSerializer02(many=True)

    class Meta:
        model = Message
        fields = ["id", "sender", "content", "visualized_by", "created_at"]
