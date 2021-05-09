from django.urls import path
from .import views


urlpatterns = [
    path('', views.add_post, name='add_post'),
    path('img/', views.img, name='img'),
]
