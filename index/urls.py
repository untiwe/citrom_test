from django.urls import path
from index.views import *


urlpatterns = [
    path('', Index.as_view(), name='index'),
    path('new_page_posts/', IndexNewPage.as_view(), name='index_new_page'),
    # path('robots.txt', robots_txt),
]
