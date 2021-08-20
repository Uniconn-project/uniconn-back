from core.generic_views import http_404_not_found
from django.urls import path, re_path

from .views import *

urlpatterns = [
    path("get-chats-list", get_chats_list),
    path("get-chat-messages/<int:chat_id>", get_chat_messages),
    path("create-message/<int:chat_id>", create_message),
    path("create-chat", create_chat),
    re_path(r".*", http_404_not_found),
]
