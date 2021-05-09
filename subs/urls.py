from django.urls import path
from subs.views import *


urlpatterns = [
    path('', Subs.as_view(), name='subs'),
    path('new_page_posts/', SubsNewPage.as_view(), name='subs_new_page'),
]
