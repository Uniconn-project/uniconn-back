from django.urls import path

from . import views

urlpatterns = [
    path("<str:user_type>/post-signup", views.signup_view),
]
