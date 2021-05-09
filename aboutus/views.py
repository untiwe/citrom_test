from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from mymodels.models import AdminMessages, CustomUser
from django.views.generic.base import View
from django.forms.models import model_to_dict
from .package import send_mail

from .forms import AdminMessagesForm
from mypackage.MixinClasses import GetUserMixin

class AboutUs(FormView, GetUserMixin):
    '''Класс вывода страницы с правилами и формы обратной связи'''
    form_class = AdminMessagesForm
    template_name = 'aboutus/about_us.html'
        
    def post(self, request, *args, **kwargs):
        user_login = self.get_user_session()
       
        post_dict = request.POST.copy()#делаем копию что бы можно было поменять пользователя
      

        if user_login: #если отправитель был залогинен
            post_dict['user_username'] = user_login
        
        form = AdminMessagesForm(post_dict)
        username = request.POST.get('name')



        if username == '': #Если именни отправителя нет
            username = 'большое'
        form.save()
        send_mail()

        return render(request, 'aboutus/about_us.html', context={'massage' : F'Спасибо {username}, мы успешно приняли вашу заявку'})