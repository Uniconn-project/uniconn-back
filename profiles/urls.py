from django.urls import path

from .views import *

urlpatterns = [
    path("<str:user_type>/post-signup", signup_view),
    path("get-my-profile", get_my_profile),
]
