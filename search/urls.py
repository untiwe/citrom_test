from django.urls import path
from search.views import *
# from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', Search.as_view(), name='search'),
    path('searchlist/', SearchList.as_view(), name='searchlist'),
]
