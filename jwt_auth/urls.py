from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import *

urlpatterns = [
    path("", Login.as_view(), name="token"),
    path("refresh/", RefreshToken.as_view(), name="token-refresh"),
    path("logout/", Logout.as_view(), name="logout"),
]
