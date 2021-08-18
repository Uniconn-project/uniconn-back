from django.db import models
from profiles.models import Profile


class Chat(models.Model):
    """
    Chats table
    """

    members = models.ManyToManyField(Profile, related_name="chats", blank=True)

    def __str__(self):
        return ", ".join([member.user.username for member in self.members.all()[:5]])


class Message(models.Model):
    """
    Messages table
    """

    chat = models.ForeignKey(Chat, related_name="messages", on_delete=models.CASCADE, blank=True, null=True)
    sender = models.ForeignKey(Profile, related_name="sent_messages", on_delete=models.SET_NULL, blank=True, null=True)
    content = models.CharField(max_length=1000, blank=True)
    visualized_by = models.ManyToManyField(Profile, related_name="visualized_messages", blank=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.sender.user.username} - {self.content[:100]}"
