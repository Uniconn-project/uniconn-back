from django.urls import path

from .views import *

urlpatterns = [
    path("<str:user_type>/post-signup", signup_view),
    path("get-my-profile", get_my_profile),
    path("get-profile/<str:slug>", get_profile),
    path("get-profile-projects/<str:slug>", get_profile_projects),
    path("get-mentor-markets/<str:slug>", get_mentor_markets),
    path("get-filtered-profiles/<str:query>", get_filtered_profiles),
    path("get-profile-list", get_profile_list),
    path("get-notifications", get_notifications),
    path("get-notifications-number", get_notifications_number),
    path("reply-project-invitation", reply_project_invitation),
    path("reply-project-entering-request", reply_project_entering_request),
]
