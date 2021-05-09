from django.urls import path
from post.views import *
# from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('<int:post_pk>/', Post.as_view(), name='post'),
    path('commentphoto/', CommentPhoto, name='commentphoto'),
    path('newcomment/', NewComment, name='newcomment'),
    path('<int:post_pk>/getcommentspost/', GetCommentsPost.as_view(), name='get_comments_post'),
]
