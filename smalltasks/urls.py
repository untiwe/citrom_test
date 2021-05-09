from django.urls import path
from smalltasks.views import *
# from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('eval_post/', eval_post, name='eval_post'),
    path('eval_comment/', eval_comment, name='eval_comment'),
    path('post_views_counter/', post_views_counter, name='post_views_counter'),
]
