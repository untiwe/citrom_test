from django.urls import path
from commentmanager.views import *
# from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('delete/', CommentDelete.as_view(), name='post_delete'),
]
