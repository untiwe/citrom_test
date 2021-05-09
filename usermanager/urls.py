from django.urls import path
from .import views
# from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('reg/', views.reg, name='reg'),
    path('change_password/', views.change_password, name='change_password'),
    path('info_user/', views.info_user, name='info_user'),
    path('add_tags/', views.add_tags, name='add_tags'),
    path('delete_tags/', views.delete_tags, name='delete_tags'),
    path('new_avatar/', views.new_avatar, name='new_avatar'),
    path('del_avatar/', views.del_avatar, name='del_avatar'),
    path('reset_password/', views.reset_password, name='reset_password'),
]
