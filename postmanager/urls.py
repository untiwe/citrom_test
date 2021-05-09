from django.urls import path
from postmanager.views import *
# from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('delete/', PostDelete.as_view(), name='post_delete'),
]
