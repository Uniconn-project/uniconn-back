from django.urls import path

from .views import *

urlpatterns = [
    path("get-markets-name-list", get_markets_name_list),
    path("get-project-list", get_project_list),
]
