from core.generic_views import http_404_not_found
from django.urls import path, re_path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import *

urlpatterns = [
    path("", Login.as_view()),
    path("refresh/", RefreshToken.as_view()),
    path("logout/", Logout.as_view()),
    re_path(r".*", http_404_not_found),
]
