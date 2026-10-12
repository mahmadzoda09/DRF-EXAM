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
    path("posts/author-statistics/", author_statistics),
    path("likes/", like_list),
    path("likes/top-posts/", top_posts),
    path("likes/<int:pk>/", like_delete),
    path("favorites/",favorite_list),
    path("favorites/<int:pk>/",favorite_delete),
    path("dashboard/",dashboard),
    path("users/<int:pk>/analytics/", user_analytics),
]
