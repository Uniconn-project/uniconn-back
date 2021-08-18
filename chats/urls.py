from core.generic_views import http_404_not_found
from django.urls import path, re_path

from .views import *

urlpatterns = [
    path("get-chats-list", get_chats_list),
    re_path(r".*", http_404_not_found),
]
