from core.generic_views import http_404_not_found
from django.urls import path, re_path

from .views import *

urlpatterns = [
    path("get-fields-name-list", get_fields_name_list),
    path("get-projects-list", get_projects_list),
    path("get-filtered-projects-list", get_filtered_projects_list),
    path("get-projects-categories-list", get_projects_categories_list),
    path("create-project", create_project),
    path("get-project/<int:project_id>", get_project),
    path("edit-project/<int:project_id>", edit_project),
    path("invite-users-to-project/<int:project_id>", invite_users_to_project),
    path("uninvite-users-from-project/<int:project_id>", uninvite_user_from_project),
    path("ask-to-join-project/<int:project_id>", ask_to_join_project),
    path("remove-users-from-project/<int:project_id>", remove_user_from_project),
    path("reply-project-invitation", reply_project_invitation),
    path("reply-project-entering-request", reply_project_entering_request),
    path("edit-project-description/<int:project_id>", edit_project_description),
    path("star-project/<int:project_id>", star_project),
    path("unstar-project/<int:project_id>", unstar_project),
    path("leave-project/<int:project_id>", leave_project),
    path("create-link/<int:project_id>", create_link),
    path("delete-link/<int:link_id>", delete_link),
    path("create-tool/<int:project_id>", create_tool),
    path("delete-tool/<int:tool_id>", delete_tool),
    path("create-project-discussion/<int:project_id>", create_project_discussion),
    path("get-project-discussions/<int:project_id>", get_project_discussions),
    path("get-project-discussion/<int:discussion_id>", get_project_discussion),
    path("delete-project-discussion", delete_project_discussion),
    path("star-discussion/<int:discussion_id>", star_discussion),
    path("unstar-discussion/<int:discussion_id>", unstar_discussion),
    path("reply-discussion/<int:discussion_id>", reply_discussion),
    path("delete-discussion-reply/<int:reply_id>", delete_discussion_reply),
    re_path(r".*", http_404_not_found),
]
