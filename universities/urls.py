from django.urls import path

from .views import *

urlpatterns = [
    path("get-universities-name-list", get_universities_name_list),
]
