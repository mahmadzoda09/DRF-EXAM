from django.urls import path
from .views import *

urlpatterns = [
    path("users/", user_list),
    path("users/<int:pk>/", user_detail),
    path("users/most-active/", most_active_users),
    path("users/statistics/", user_statistics),
]
