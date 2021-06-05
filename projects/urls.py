from django.urls import path

from .views import *

urlpatterns = [
    path("get-markets-name-list", get_markets_name_list),
    path("get-projects-list", get_projects_list),
    path("get-filtered-projects-list", get_filtered_projects_list),
    path("get-projects-categories-list", get_projects_categories_list),
    path("create-project", create_project),
    path("get-project/<int:project_id>", get_project),
    path("edit-project/<int:project_id>", edit_project),
]
