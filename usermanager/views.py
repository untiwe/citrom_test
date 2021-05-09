import re
from datetime import date

from django.contrib.auth import (authenticate, login, logout,
                                 update_session_auth_hash)
from django.contrib.auth.hashers import check_password
from django.contrib.auth.password_validation import *
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import render
from mymodels.models import CustomUser, Profile, SubTags, Tags
from mypackage.pakage import get_user_session
from citrom.settings import BASE_DIR
from .forms import *
from django.core.mail import EmailMessage
from .package import gen_new_password

# уроки регистрации https://www.youtube.com/watch?v=lqgOUWSNSfE
# смена пароля через классы https://www.youtube.com/watch?v=cBYAa_kI_Bk
# manage.py shell вход в консоль
# User.objects.filter(username__iexact=username) проверка без регистра логина
# User.objects.filter(username__iexact=email) проверка без регистра емайла

default_src = '/default_avatar.svg'

def _is_18_age(birth):

    '''Функция получется значени поля birth модели Profile и проверяет наличие 18-ти лет'''

    if birth == None:#если день рожденья не уствновлен
        return False
    today = date.today()
    age =  today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))
    if age >= 18:
        return True
    return False


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)  # data обязательна
        # проверка на наличие логина/пароля
        if authenticate(username=request.POST['username'], password=request.POST['password']) is not None:
            if form.is_valid():
                user = form.get_user()
                login(request, user)
                respose = render(request, 'usermanager/login.html')
                if _is_18_age(Profile.objects.get(user_base=user).birth):#проверяем пользователся по базе и вешаем куки если есть 18
                    respose.set_cookie(key='is_18_age', value=True, expires='Tue, 1 Jan 2100 00:00:00 GMT')

                return respose
        return HttpResponse('error:Неверный логин или пароль')
        
    return render(request, 'usermanager/login.html')


def user_logout(request):
    logout(request)
    form = UserLoginForm()
    respose = render(request, 'usermanager/login.html', {'form': form})
    respose.delete_cookie(key='is_18_age')
    return respose


def reg(request):


    if request.method == 'POST':
        # проверка на "правильные" символы
        regex = re.findall(r'[0-9A-Za-z\-\_]', request.POST['username'])
        len_username = len(request.POST['username'])
        if len(regex) != len_username:
            return HttpResponse("error:Только английские буквы, цифры и знаки '-' '_' в логине")
        
        if len_username > 30:
            return HttpResponse("error:Логин не больше 30-ти символов")

        # Делаем проверку на username и email без учета регистра
        if CustomUser.objects.filter(username__iexact=request.POST['username']).exists():
            return HttpResponse('error:Такой пользователь уже существует')
        if CustomUser.objects.filter(email__iexact=request.POST['email']).exists():
            return HttpResponse('error:Такой email уже зарегистрирован')

        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()  # сохранем нового пользователя
            login(request, user)  # срузу же логинем его
            return render(request, 'usermanager/login.html')
        else:
            # Если не прошла валидность
            out_error = ''
            errors = form.errors.as_data()  # вытаскиваем причину ошибки из массива в форме data
            for text_measge in errors:
                out_error += str(errors[text_measge][0])
            out_error = 'error:' + out_error
            return HttpResponse(out_error)  # Отправляем прчину ошибки
            #messages.error(request, 'Случилась ошибка')
    else:
        form = UserRegisterForm()
    return render(request, 'usermanager/reg.html', {'form': form})


def change_password(request):
    if request.method == 'POST':
        user = CustomUser.objects.get(username=request.user)
        old_password = request.POST["old_password"]
        new_pass = request.POST["new_password"]
        new_pass_rep = request.POST["new_password_repeat"]
        # делаем валидацию пароля
        try:
            validate_password(new_pass, user)
        except ValidationError as error:
            # Если валидация не прошшла, вызывается ошибка. Перехватываем и отправляет ее текст
            return HttpResponse('error:%s' % (error))

        if new_pass != new_pass_rep:
            return HttpResponse('error:Пароли не совпадают')
        if new_pass == old_password:
            return HttpResponse('error:Страый и новый пароль не отличаются')
        if check_password(old_password, user.password):
            user.set_password(request.POST["new_password_repeat"])
            user.save()
            # для обновления сессии после смены паролья, используем update_session_auth_hash(запрос, пользователь из модели(базы))
            update_session_auth_hash(request, user)
            return HttpResponse('ok')
        else:
            return HttpResponse('error:Не верный пароль')


def info_user(request):
    '''Обновляем данные о пользователе. Имя, дата рождения, пол, информация о себе'''
    if request.method != 'POST':
        return HttpResponse('я жду POST')
    
    response = HttpResponse('ok')
    
    profile = Profile.objects.get(
        user_base=request.user)

    profile.user_base.first_name = request.POST.get('first_name')
    profile.gender = request.POST.get('gender')
    profile.about = request.POST.get('about')

    year_birth = request.POST.get('year_birth')
    month_birth = request.POST.get('month_birth')
    day_birth = request.POST.get('day_birth')

    if year_birth and month_birth and day_birth:
        profile.birth = date(int(year_birth), int(month_birth), int(day_birth))
        if _is_18_age(profile.birth):#пишем куки если есть 18
            response.set_cookie(key='is_18_age', value=True, expires='Tue, 1 Jan 2100 00:00:00 GMT')
        else:#или удаляем(если их нет, ошибкт не будет)
            response.delete_cookie(key='is_18_age')
        


    if not year_birth or not month_birth or not day_birth:  # если хоть одно поле пустое
        if not year_birth and not month_birth and not day_birth:  # и путсые поля - все 3
            profile.birth = None  # сбразывает дату рожденя
            response.delete_cookie(key='is_18_age')
        else:
            # или дата не корректная
            return HttpResponse('error:Не корректная дата')

    profile.user_base.save()
    profile.save()
    return response


def add_tags(request):
    '''Добавлние тегов в список. На блокировку или подписку, в зависимости от command'''
    if request.method != 'POST':
        return HttpResponse('я жду POST')

    if request.POST.get('command') == 'true':
        command = True
    if request.POST.get('command') == 'false':
        command = False
    tag, _ = Tags.objects.get_or_create(tag=request.POST.get('tag'))
    user = CustomUser.objects.get(username=request.user)

    SubTags.objects.create(tag_id=tag, user_id=user, status=command)

    return HttpResponse('ok')

def delete_tags(request):
    '''Удаление тегов из списка. На блокировку или подписку, в зависимости от command'''
    if request.method != 'POST':
        return HttpResponse('я жду POST')

    if request.POST.get('command') == 'true':
        command = True
    elif request.POST.get('command') == 'false':
        command = False
    else:
        return HttpResponse('error:Неизвестная ошибка')
    

    tag = Tags.objects.get(tag=request.POST.get('tag'))
    user = CustomUser.objects.get(username=request.user)
    SubTags.objects.filter(tag_id=tag, user_id=user, status=command).delete()

    return HttpResponse('ok')

def new_avatar(request):
    '''Обновляем аватар пользователя'''
    if request.method != 'POST':
        return HttpResponse('я жду POST')

    user = get_user_session(request)

    if user == False:
        return HttpResponse('error:Вы не авторизованы')
    
    if  user.profile.avatar != default_src:
        user.profile.avatar.delete(save=False)#Удаляем старый файл аватара


    user.profile.avatar = request.FILES['photo']
    user.save()
    cache.delete(F'avatar_{user}')#Удаляем старый аватар из кэша
    return HttpResponse(user.profile.avatar.url)

def del_avatar(request):
    '''Уствновка аватара пользователя на стандартный'''
    
    if request.method != 'POST':
        return HttpResponse('я жду POST')
    user = get_user_session(request)
    if user == False:
        return HttpResponse('Вы не авторизованы')

    if  user.profile.avatar != default_src:
        user.profile.avatar.delete(save=False)#Удаляем старый файл аватара

    
    user.profile.avatar = default_src;
    user.save()
    cache.delete(F'avatar_{user}')#Удаляем аватар из кэша
    return HttpResponse(user.profile.avatar.url)

def reset_password(request):
    '''Уcтановка нового пароля и отправка его на email пользователя'''
    print()
    if request.method != 'POST':
        return HttpResponse('я жду POST')
    user_email = request.POST.get('email')
    if not CustomUser.objects.filter(email__iexact = user_email).exists():
        return HttpResponse('error')

    new_password = gen_new_password()
    user = CustomUser.objects.get(email__iexact = user_email)
    user.set_password(new_password)
    user.save()

    email = EmailMessage(
        subject = 'Сброс пароля Citrom',
        body = F'Привет! Ты тут пароль потерял. Вот тебе новый: {new_password}',
        from_email = 'info@citrom.ru',
        to = (user_email,)
    )
    
    email.send()
    


    return HttpResponse('ok')
