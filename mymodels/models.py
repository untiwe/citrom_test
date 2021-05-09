# Create your models here.

import datetime

from django.conf import settings
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.db.models.signals import post_delete, post_save
from django.dispatch.dispatcher import receiver
from django.urls import reverse
import json
# python manage.py makemigrations
# python manage.py migrate


class CustomUserManager(UserManager):
    '''
    Кастомный юзер, вместо обычного. Сделан для регистронезависимого залогинивания
    '''

    def get_by_natural_key(self, username):
        case_insensitive_username_field = '{}__iexact'.format(
            self.model.USERNAME_FIELD)
        return self.get(**{case_insensitive_username_field: username})

    

class CustomUser(AbstractUser):
    objects = CustomUserManager()

    group  = models.SmallIntegerField(default=100,
                                     help_text='Номер группы пользователя. 100 - обычный пользователь')
    
    def get_absolute_url(self):
        return reverse('user_view', kwargs={'username': self.username})



class Profile(models.Model):

    '''
    Расширение стандартной модлеи user. Привязано к пользователю соотношением "один к одному"  
    В базовой таблице user уже есть:
    - username
    - email
    - first_name
    - date_joined
    '''

    user_base = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                     help_text='Связь со стандартной моделью пользовтеля')
    user_rating = models.IntegerField(default=0,
                                        help_text='Рейтинг пользователя')
    avatar = models.ImageField(upload_to='avatars/%Y/%m/%d/', default='/default_avatar.svg',
                               help_text='Аватар пользователя')
    choices_gender = [
        ('',  ''),
        ('Male',  'Муж'),
        ('Female',  'Жен'),
    ]
    gender = models.CharField(
        max_length=6,
        choices=choices_gender,
        default='',
    )
    birth = models.DateField(null=True,
                             help_text='Дата рождения пользолвателя')
    about = models.TextField(max_length=1000, blank=True,
                             help_text='"О себе"')
    messages_count = models.BooleanField(default=0,
                                         help_text='1 если есть новые сообщения')
    



@receiver(post_delete, sender=Profile)
def delete_avatar_profile(sender, instance, **kwargs):
    '''Удаление аватара пользователя, если он не стандартный'''
    if instance.avatar != '/default_avatar.svg':
        instance.avatar.delete(False)
        

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user_base=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Messages(models.Model):

    '''
    Сообщения(уведомления) которые получают пользователи от админимстрации сайта, или по событию.
    '''

    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True, default=None,
                                help_text='Получаеть сообщения')
    type = models.CharField(max_length=100, blank=True,
                               help_text='Тип сообщения')
    text = models.TextField(max_length=3000,
                            help_text='Объект сообщения')
    date_create = models.DateTimeField(auto_now_add=True,
                                   help_text='Дата создания')

    def __str__(self):
        return F'Сообщение {self.type} для {self.user_id}'


class AdminMessages(models.Model):

    '''Сюда приходят все сообщения со страницы aboutus т.е. все сообщения к админимтрации. Если пишет юзер, 
    его имя будет в поле user_username.'''

    user_username = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True, default=None, verbose_name='Пользователь',
                                help_text='Связь со стандартной моделью пользовтеля, может быть null')
    name = models.CharField(max_length=150, blank=True, default=None, verbose_name='Как обращаться',
                                help_text='Input "Как обращаться"')
    contacts = models.CharField(max_length=500, blank=True, default=None, verbose_name='Контакты',
                                help_text='Input "Способ связи"')
    text = models.TextField(max_length=3000, verbose_name='Сообщение',
                                help_text='Текст сообщения')
    date_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата сообщения',
                                help_text='Дата создания')

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'Сообщения'
        verbose_name_plural = 'Сообщения'

class Posts(models.Model):

    '''
    Модель поста. Сюда пишеся сам пост и его параметры. Хоть в блоке content и есть url картинок, сами картинки хронятся в своей, отдельной модели.
    '''

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, default='', verbose_name='Автор',
        help_text='Автор поста')
    name = models.CharField(max_length=150, verbose_name='Название', 
                                help_text='Название поста')
    content = models.TextField(help_text='Контент поста', verbose_name='Контент', default='no')
    views = models.IntegerField(default=0, verbose_name='Просмотры',
                                help_text='Счеттчик просмотров')
    post_rating = models.IntegerField(default=0, verbose_name='Рейтинг',
                                      help_text='Рейтинг поста')
    date_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания',
                                       help_text='Дата создания')

    def __str__(self):
        return self.name

    def get_content_dict(self):
        '''
        В базу записывается словарь в формате JSON. Но python по умочанию, видит ее как строку. Функция превращает ее в словарь
        Для того, что бы python видел ее как объект нужная другая БД с поддержкой JSONField
        '''
     
        return json.loads(self.content)
            

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_pk': self.id})

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'



class ViewsPosts (models.Model):
    '''
    Просмотры постов у пользователей
    '''
    post_id = models.ForeignKey(Posts, on_delete=models.CASCADE,
                                help_text='Связь, с постом, которому относится просмотри')
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                help_text='Связь с пользователем, который просмотрел')
    date_update = models.DateTimeField(auto_now=True,
                                    help_text='Дата просмотра')
    class Meta:#делаем уникальное сочетание полей
        unique_together = ('post_id', 'user_id')

    def __str__(self):
        return 'Пост %s пользователь %s' % (self.post_id, self.user_id)
    
class DeletedPosts (models.Model):
    '''
    Удаленные посты. Связь каждого экземпляра с постом по типу "один к одному"
    '''

    post_deleted = models.OneToOneField(Posts, on_delete=models.CASCADE,
                                    help_text='Связь с с постом')
    user_deleted = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_DEFAULT, blank=True, null=True, default=None,
                                    help_text='Модератор/автор, удаливший пост')
    cause = models.CharField(max_length=500, blank=True,
                                    help_text='Краткая причина удаления')
    full_cause = models.TextField(blank=True, 
                                    help_text='Полная причина удаления')
    date_deleted = models.DateTimeField(auto_now_add=True,
                                    help_text='Дата удаления')
    def __str__(self):
        return F'Пост: {self.post_deleted} Удалил: {self.user_deleted}'


class Tags(models.Model):

    '''
    Модель тегов. По сути это просто список тегов, кторые используются хотя бы в одном посте.
    '''

    tag = models.CharField(max_length=60, unique=True, verbose_name='Тег',
                           help_text='Имя тега поста')
    posts = models.ManyToManyField(
        Posts, help_text='Свзять "Многих ко многим", тегов с постами"')
    count_posts = models.IntegerField(default=0, verbose_name='Счетчик постов',
                                      help_text='Счетчике постов')

    def __str__(self):
        return self.tag

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

class SubTags(models.Model):

    '''
    Модель подписаных тегов. Похожа на промежуточную модель для ManyToMany но есть еще пара полей. Служит для хранения подписаных и забаненых тегов пользователей.
    '''

    tag_id = models.ForeignKey(Tags, on_delete=models.CASCADE,
                               help_text='Свзять с тегом из таблицы тегов')
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                help_text='Свзять с пользователем из таблицы пользователей')
    status = models.BooleanField(
        help_text='Булевое знгачение. 0 = бан, 1 = подписка, нету записи = ничего')

    def __str__(self):
        return str(self.tag_id)


class Comments(models.Model):

    '''
    Модель комментариев. Хранит основные свойства комментария.
    '''

    post_id = models.ForeignKey(Posts, on_delete=models.CASCADE,
                                help_text='Свзять, коментариев с постами', verbose_name='К постам')
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, default='', verbose_name='Автор', 
                                help_text='Свзять, коментариев с их авторами')
    perent_comment_id = models.ForeignKey('self', on_delete=models.CASCADE, null=True, default=None, verbose_name='К комментарию',
                                          help_text='id "родительского" комментария, может быть пустым')
    content = models.TextField(
        help_text='Текст самого комментария', default='')
    comment_rating = models.IntegerField(default=0, verbose_name='Рейтинг',
                                         help_text='Рейтинг комментария')
    date_create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания',
                                       help_text='Дата создания')

    def __str__(self):
        # выводит контет комментария в "сыром" виде. Надо бы нормальный обработчик для вывода сделать...
        return str(self.pk)
    
    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class EvaluationComments (models.Model):

    '''
    Оценки коментариев.Похожа на промежуточную модель для ManyToMany но есть еще поле для хранения оценки
    '''

    comment_id = models.ForeignKey(Comments, on_delete=models.CASCADE,
                                   help_text='Комментарий, к которому относится оценка')
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                help_text='пользователь, к который оставил оценку')
    evaluation = models.BooleanField(
        help_text='Какая именно оценка. 0 = плохая, 1 = хорошая')
    date_set = models.DateTimeField(auto_now_add=True,
                                    help_text='Дата оценки')

    def __str__(self):
        return 'Оценка комментария %s' % (self.evaluation)

class DeletedComments (models.Model):
    '''
    Удаленные комментарии. Связь каждого экземпляра с комментарием по типу "один к одному"
    '''

    comment_deleted = models.OneToOneField(Comments, on_delete=models.CASCADE,
                                    help_text='Связь с комментарием')
    user_deleted = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_DEFAULT, blank=True, null=True, default=None,
                                    help_text='Модератор/автор, удаливший комментарий')
    cause = models.CharField(max_length=500, blank=True,
                                    help_text='Краткая причина удаления')
    full_cause = models.TextField(blank=True, 
                                    help_text='Полная причина удаления')
    date_deleted = models.DateTimeField(auto_now_add=True,
                                    help_text='Дата удаления')
    def __str__(self):
        return F'Комментарий: {self.comment_deleted} Удалил: {self.user_deleted}'


class CommentsPhotos (models.Model):

    '''
    Модель для храения фотографий для комментариев. Со связью один к одному.
    '''

    photo = models.ImageField(upload_to="comments/%Y/%m/%d/", height_field=None, width_field=None, max_length=None,
                              help_text='Поле с url сохраненной фотографии коментария')
    сomment_id = models.ForeignKey(Comments, on_delete=models.CASCADE,
                                   help_text='Связь, с коментарием, которому пренадлежит фото', null=True, default=None)
    date_create = models.DateTimeField(auto_now_add=True,
                                       help_text='Дата создания')

    def __str__(self):
        # Просто объект photo это ОБЪЕКТ а не строка, по этому выводим ИМЕЕНО ЕГО name
        # return 'Фото комментария %s' % (self.photo.name)
        return self.photo.name

    
@receiver(post_delete, sender=CommentsPhotos)
def comment_photo_delete(sender, instance, **kwargs):
    '''Удаления фотографии комментария'''
    instance.photo.delete(False)

class PostsPhotos (models.Model):

    '''
    Модель для храения фотографий для постов.
    '''

    photo = models.ImageField(upload_to='posts/%Y/%m/%d/', height_field=None, width_field=None, max_length=None,
                              help_text='Поле с url сохраненной фотографии поста')

    post_id = models.ForeignKey(Posts, on_delete=models.CASCADE,
                                help_text='Связь, с постом, которому пренадлежит фото', null=True, default=None)
    date_create = models.DateTimeField(auto_now_add=True,
                                       help_text='Дата создания')

    # переопределение save() на стандартное(без изменений)
    # def save(self, username='', *args, **kwargs):
    #     super().save(*args, **kwargs)

    def __str__(self):
        # Просто объект photo это ОБЪЕКТ а не строка, по этому выводим ИМЕЕНО ЕГО name
        return 'Фото поста %s' % (self.photo.name)

@receiver(post_delete, sender=PostsPhotos)
def post_photo_delete(sender, instance, **kwargs):
    '''Удаления фотографии поста'''
    instance.photo.delete(False)

class EvaluationPosts (models.Model):
    '''
    Оценки постов.Похожа на промежуточную модель для ManyToMany но есть еще поле для хранения оценки
    '''
    post_id = models.ForeignKey(Posts, on_delete=models.CASCADE,
                                help_text='Связь, с постом, которому относится отценка')
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                help_text='пользователь, к который оставил оценку')
    evaluation = models.BooleanField(
        help_text='Какая именно оценка. 0 = плохая, 1 = хорошая')
    date_set = models.DateTimeField(auto_now_add=True,
                                    help_text='Дата оценки')

    def __str__(self):
        return 'Оценка поста %s' % (self.evaluation)
