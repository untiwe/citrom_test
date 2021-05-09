from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from mymodels.models import CustomUser, Posts
# Create your views here.


class BaseSitemap(TemplateView):
    '''Класс возваращает первую страницу sitemap '''
    content_type = 'application/xml'
    template_name = 'sitemap/base_sitemap.xml'

class StaticSitemap(TemplateView):
    '''Класс возваращает sitemap неизменяемыми страницами'''
    content_type = 'application/xml'
    template_name = 'sitemap/static_sitemap.xml'



#классы для постов
class ExcludeDelPostsMixin():
    '''Миксин для удаления удаленных посто из запроса'''

    def exclude_del_posts(self, queryset):
        '''Принимаем запрос постов и добавляем в него исключение удаленных. Возвращаем'''
     
        queryset = queryset.exclude(deletedposts__post_deleted__gte = 0)
        return queryset

class GetRawObjectMixin():
    '''Класс для возврата начального запроса обектов '''

    def get_raw_object(self):
        '''Возвращаем начальный запрос, без доп фильторв'''
        return self.exclude_del_posts(Posts.objects.all())#убираем из списка удаленные посты

class ListsPostsBaseSitemap(TemplateView, ExcludeDelPostsMixin, GetRawObjectMixin):
    '''Класс для вывода sitemaps групп постов'''
    template_name = 'sitemap/lists_objects_base.xml'
    content_type = 'application/xml'
    slise_count = 1000 #ссыков в олдном sitemap
    extra_context = {'list_name' : 'posts'}
    count_objects = 0 #просто объявление, потом сюда пишется количество объектов
    
    def str_construct(self, i):
            '''Конструктор строки для среза группы, пример: "11-20"'''
            if i + self.slise_count > self.count_objects:
                return F'{i}-{self.count_objects}'

            return F'{i}-{i+(self.slise_count-1)}'

    def get_raw_object(self):
        '''Возвращаем начальный запрос, без доп фильторв'''
        return self.exclude_del_posts(Posts.objects.all())#убираем из списка удаленные посты

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        queryset = self.get_raw_object()
        self.count_objects = queryset.count()

       

        list_slises = [self.str_construct(i) for i in range(1, self.count_objects+1, self.slise_count)]
        context['list_slises'] = list_slises

        return context

class ListsPostsSitemap(ListView, ExcludeDelPostsMixin, GetRawObjectMixin):
    '''Собираем группу постов от start до stop'''
    template_name = 'sitemap/lists_posts_sitemap.xml'
    content_type = 'application/xml'
    
    #чем старше пост, тем больше частота обновления она ставится в завичимости от id поста
    #"правильнее" высчитывать дату добавления поста, но этот способ менее ресурсозатратный.
    #а обновление "старых" id можно автоматичски обновлять, допустим раз в неделю
    old = 20 #посты меньше этого id считаются старыми
    must_old = 10 #посты меньше этого id считаются очень старыми

    def get_queryset(self):
        st = self.kwargs['start']-1 #срезы считаются от +1, по этому тут -1
        sp = self.kwargs['stop']
        queryset = self.get_raw_object()
        return queryset[st:sp]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['old'] = self.old
        context['must_old'] = self.must_old

        return context
    

#классы для пользователей
class ListsUsersBaseSitemap(ListsPostsBaseSitemap):
    '''Класс для вывода sitemaps групп постов'''
    model = CustomUser
    extra_context = {'list_name' : 'users'}
    

    def get_raw_object(self):
        '''Возвращаем начальный запрос, без доп фильторв'''
        return CustomUser.objects.all()

class ListsUsersSitemap(ListsPostsSitemap):
    '''Собираем группу пользователей от start до stop'''
    template_name = 'sitemap/lists_users_sitemap.xml'
    model = CustomUser
    

    def get_raw_object(self):
        '''Возвращаем начальный запрос, без доп фильторв'''
        return CustomUser.objects.all()
    
    


