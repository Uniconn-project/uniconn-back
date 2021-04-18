from django.urls import path

from .views import *

urlpatterns = [
    path("<str:user_type>/post-signup", signup_view),
    path("is-auth", get_is_auth)
]
