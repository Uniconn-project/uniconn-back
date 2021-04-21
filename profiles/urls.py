from django.urls import path

from .views import *

urlpatterns = [
    path("<str:user_type>/post-signup", signup_view),
    path("<str:user_type>/get-my-profile", get_my_profile),
]
