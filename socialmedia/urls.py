from django.urls import path
from .views import *

urlpatterns = [
    path("users/", user_list),
    path("users/<int:pk>/", user_detail),
    path("users/most-active/", most_active_users),
    path("users/statistics/", user_statistics),
    path("profiles/", profile_list),
    path("profiles/city-statistics/", city_statistics),
    path("profiles/<int:pk>/", profile_detail),
    path("posts/", post_list),
    path("posts/popular/", popular_posts),
    path("posts/search/", post_search),
    path("posts/filter/", post_filter),
    path("posts/statistics/", post_statistics),
    path("posts/<int:pk>/", post_detail),
]
