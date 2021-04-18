from django.urls import path

from .views import *

urlpatterns = [path("get-markets-name-list", get_markets_name_list)]
