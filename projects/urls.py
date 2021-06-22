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
    path("invite-<str:type>-to-project/<int:project_id>", invite_users_to_project),
    path("uninvite-<str:type>-from-project/<int:project_id>", uninvite_user_from_project),
    path("ask-to-join-project/<int:project_id>", ask_to_join_project),
    path("remove-<str:type>-from-project/<int:project_id>", remove_user_from_project),
    path("reply-project-invitation", reply_project_invitation),
    path("reply-project-entering-request", reply_project_entering_request),
    path("edit-project-description/<int:project_id>", edit_project_description),
    path("create-link/<int:project_id>", create_link),
    path("delete-link", delete_link),
]
