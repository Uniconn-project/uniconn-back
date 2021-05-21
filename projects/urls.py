from django.urls import path

from .views import *

urlpatterns = [
    path("get-markets-name-list", get_markets_name_list),
    path("get-projects-list", get_projects_list),
    path("get-projects-categories-list", get_projects_categories_list),
]
