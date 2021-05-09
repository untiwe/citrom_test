import json

from django.db.models import Q
from django.http import HttpResponse
from django.views import View
from mymodels.models import Posts, CustomUser
from mypackage.MixinClasses import GetUserMixin, SlicerMixin, ExcludeDelPostsMixin
import datetime
from django.utils import timezone



class PostsList(View, SlicerMixin, GetUserMixin, ExcludeDelPostsMixin):
    '''Базовый клас для отображения списка постов в тех или иных местах сайта, включая главную. Не используется ListView т.к. там запрещен POST'''
    posts_in_page = 5
    model = Posts
    template_name = 'index/post_list.html'
    context_object_name = 'posts'
    
   

    def get_tags_filter(self):
        '''Смотрит куки и возвращет спиок запрещенных постов'''
        cookies = self.request.COOKIES
        out_list = ['nsfw', 'политика', 'жесть']
        if cookies.get('is_18_age') and cookies.get('nsfw'):
            out_list.remove('nsfw')
        if cookies.get('politic'):
            out_list.remove('политика')
        if cookies.get('gore'):
            out_list.remove('жесть')

        return out_list
    
    
    def get_tags_user(self, value=True):
        '''Возвращает список подписаных или забаненых тегов пользователя в зависимоти от value'''
        user = self.get_user_session()
        if user==False:
            return []

        list_tags = user.subtags_set.filter(status = value).values('tag_id__tag')
        list_tags = [key['tag_id__tag'] for key in list_tags]

        return list_tags
        

    def get_queryset(self):
        '''Возварщает соответсвующий запрос'''
        start, end = self.get_slice(self.request, self.posts_in_page)

        list_views_posts = self.get_list_views_posts()

        block_tags = self.get_tags_filter() + self.get_tags_user(value=False)

        slice_time = timezone.now() - datetime.timedelta(days=90)  #расчитываем срез в -90 день от сегодня, напомниаю что у settings стоит USE_TZ = True

        queryset = Posts.objects.select_related('author').prefetch_related('evaluationposts_set', 'tags_set', 'comments_set')
        queryset = queryset.filter(date_create__gt=slice_time)
        queryset = queryset.exclude(Q(id__in=list_views_posts) | Q(tags__tag__in=block_tags))
        queryset = self.exclude_del_posts(queryset)
        queryset = queryset.order_by('-pk')

        return queryset[start:end]


    def get_list_views_posts(self):
        '''Возвращает массив просмотренных постов из POST если надо, или возвращает пустой массив'''
        if (self.request.COOKIES.get('hide_view')):
            return self.request.POST.getlist('views_posts[]')
        else:
            return []

    def get_posts(self):
        user = self.get_user_session()
        
        posts_list = self.get_queryset()
        
        out_data = []

        for one_post in posts_list:

            post_data = {}

            if not user:
                post_data['eval'] = 0
            # если get(), то будет кидать исключение при отсутствии объекта
            post_eval = one_post.evaluationposts_set.filter(
                user_id=user).first()
            if (post_eval == None):
                post_data['eval'] = 0
            elif post_eval.evaluation == True:
                post_data['eval'] = 1
            elif post_eval.evaluation == False:
                post_data['eval'] = -1

            tags_list = []
            for tag in one_post.tags_set.all():
                tags_list.append(tag.tag)
            post_data['tags'] = tags_list

            # В базу записывается словарь в формате JSON. Но python по умочанию, видит ее как строку.
            # для того, что бы python видел ее как объект нужная другая БД с поддержкой JSONField
            post_data['content'] = json.loads(one_post.content)
           
            # Функция превращает ее в словарь. Просто послать сроку нелья, т.к. js неадеквато ее пробразует
            post_data['name'] = one_post.name
            post_data['author'] = one_post.author.username
            post_data['avatar'] = one_post.author.profile.avatar.url
            post_data['rating'] = one_post.post_rating
            post_data['views'] = one_post.views
            post_data['comments'] = len(one_post.comments_set.all())
            post_data['post_id'] = one_post.pk
            if hasattr(one_post, 'deletedposts'): #проверка, удален ли пост, на 16.03.21 удаленные посты get_queryset() возврщает только на странице пользователя и то его собственные
                post_data['is_deleted'] = True
            
            
            if user:
                if one_post.author.username == user.username or user.group > 100:
                    post_data['may_change'] = True
            
            out_data.append(post_data)

        return json.dumps(out_data)

    

    def get(self, request, *args, **kwargs):
        return HttpResponse('Вообще то я жду POST')

    def post(self, request, *args, **kwargs):
      
        data = self.get_posts()

        return HttpResponse(data)

