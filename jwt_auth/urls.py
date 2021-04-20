from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import *

urlpatterns = [
    path("", Login.as_view()),
    path("refresh/", RefreshToken.as_view()),
    path("logout/", Logout.as_view()),
]
