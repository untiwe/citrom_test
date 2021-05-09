from django.urls import path
from newpost.views import *
# from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', NewPost.as_view(), name='new_post'),
    path('new_post_preview/', NewPostPreview.as_view(), name='new_post_preview'),
    path('save_post/', SavePost, name='save_post'),
    path('load_photo/', LoadPhoto, name='load_photo'),
    path('tags_serch/', TagsSerch, name='tags_serch'),
    path('del_post_imgs/', DelPostImgs, name='del_post_img'),
]
