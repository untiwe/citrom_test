from django.urls import path
from user.views import *
# from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('<slug:username>/', UserView.as_view(), name='user_view'),
    path('<slug:username>/help_serch_tags/', help_serch_tags, name='help_serch_tags'),
    path('<slug:username>/get_posts/', GetPosts.as_view(), name='get_posts'),
    path('<slug:username>/like_posts/', LikePosts.as_view(), name='like_posts'),
    path('<slug:username>/dislike_posts/', DislikePosts.as_view(), name='dislike_posts'),
    path('<slug:username>/get_comments_user/', GetCommentsUser.as_view(), name='get_comments_user'),
]

