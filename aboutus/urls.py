from django.urls import path
from aboutus.views import *


urlpatterns = [
    path('', AboutUs.as_view(), name='about_us'),
]
