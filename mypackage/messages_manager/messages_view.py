from django.http.response import HttpResponse, JsonResponse
from mypackage.MixinClasses import SlicerMixin, GetUserMixin, GetRequsestUserStatusMixin
from mymodels.models import Messages, CustomUser
from django.views import View
from django.shortcuts import render
from django.core.cache import cache
from django.shortcuts import get_object_or_404, redirect

class GetMessages(View, SlicerMixin, GetUserMixin, GetRequsestUserStatusMixin):
    '''Возврат комментариев пользователя'''

    messages_in_page = 10

    def get_queryset(self):
        
        user = get_object_or_404(CustomUser, username=self.kwargs['username'])
        start, end = self.get_slice(self.request, self.messages_in_page)

        return Messages.objects.filter(user_id=user).order_by('-date_create').values('text', 'date_create', 'type')[start:end]


    def get(self, request, *args, **kwargs):
        #проверка, пользователь/модератор
        user = get_object_or_404(CustomUser, username=self.kwargs['username'])
        request_user = self.get_user_session()
        if self.get_request_user_status(request_user, user) < 101:
            return redirect('/')
        
        context = {'username' : user}
        return render(request, 'messages/messages.html', context)

    def post(self, request, *args, **kwargs):

        #без проверка пользователя, она была на уровне get запроса
        
        messages = self.get_queryset()

        return JsonResponse(list(messages), safe=False)