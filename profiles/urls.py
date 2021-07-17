from core.generic_views import http_404_not_found
from django.urls import path, re_path

from .views import *

urlpatterns = [
    path("<str:user_type>/post-signup", signup_view),
    path("edit-my-profile", edit_my_profile),
    path("get-my-profile", get_my_profile),
    path("get-profile/<str:slug>", get_profile),
    path("get-profile-projects/<str:slug>", get_profile_projects),
    path("get-mentor-markets/<str:slug>", get_mentor_markets),
    path("get-filtered-profiles/<str:query>", get_filtered_profiles),
    path("get-profile-list", get_profile_list),
    path("get-skills-name-list", get_skills_name_list),
    path("get-notifications", get_notifications),
    path("get-notifications-number", get_notifications_number),
    path("visualize-notifications", visualize_notifications),
    re_path(r".*", http_404_not_found),
]
