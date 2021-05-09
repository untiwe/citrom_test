from django.urls import path
from sitemap.views import *

urlpatterns = [
    path('', BaseSitemap.as_view(), name='base_sitemap'),
    path('static_sitemap/', StaticSitemap.as_view(), name='static_sitemap'),
    path('lists_posts/', ListsPostsBaseSitemap.as_view(), name='lists_posts_base_sitemap'),
    path('lists_posts_<int:start>-<int:stop>/', ListsPostsSitemap.as_view(), name='lists_posts_sitemap'),
    path('lists_users/', ListsUsersBaseSitemap.as_view(), name='lists_users_base_sitemap'),
    path('lists_users_<int:start>-<int:stop>/', ListsUsersSitemap.as_view(), name='lists_users_sitemap'),
]
