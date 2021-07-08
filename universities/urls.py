from core.generic_views import http_404_not_found
from django.urls import path, re_path

from .views import *

urlpatterns = [
    path("get-universities-name-list", get_universities_name_list),
    path("get-majors-name-list", get_majors_name_list),
    re_path(r".*", http_404_not_found),
]
