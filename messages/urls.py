from django.urls import path
from messages.views import *
# from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('<slug:username>/', MessagesView.as_view(), name='messages_user'),
    ]