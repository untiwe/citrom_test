from django import forms
#from django.contrib.auth.models import User  # всё хорошо, хз че он ругается
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import *

from mymodels.models import CustomUser


class UserLoginForm(AuthenticationForm):
    '''
    Эта часть может зрузиться через index, дабы не громоздить там код сделал форму не автоматической. Эта UserLoginForm в принципе не нужна, оставил "на всякий случай"
    '''
    username = forms.CharField(max_length=30, label="Ваш логин",)
    password = forms.CharField(label="Пароль", )


# class UserRegisterForm(UserCreationForm):
class UserRegisterForm(UserCreationForm):
    username = forms.CharField(max_length=30, label="Ваш логин",
                               help_text="Не большое 30-ти символов",
                               widget=forms.TextInput(
                                   attrs={'class': 'user_sell input_user',
                                          'type': 'text', 'placeholder': 'Логин'}
                               ))
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput(
        attrs={'class': 'user_sell input_user',
               'type': 'password', 'placeholder': 'Пароль'}
    ))

    password2 = forms.CharField(label="Пароль еще раз", widget=forms.PasswordInput(
        attrs={'class': 'user_sell input_user',
               'type': 'password', 'placeholder': 'Пароль  еще раз'}
    ))
    email = forms.EmailField(label="Почта", widget=forms.EmailInput(
        attrs={'class': 'user_sell input_user',
               'type': 'email', 'placeholder': 'Почта'}
    ))

    

    class Meta:
        model = CustomUser
        fields = ('username', 'password1', 'password2', 'email')
