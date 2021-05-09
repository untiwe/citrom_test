from django.http import HttpResponse
from django.views.generic import TemplateView
from mypackage.MixinClasses import ExcludeDelPostsMixin
from mypackage.posts_manager.posts_list import PostsList

from .package import SearchQuerysetMixin


class Search(TemplateView, SearchQuerysetMixin, ExcludeDelPostsMixin):
    '''Отображение страницы поиск + сохранение настроек поиска'''

    template_name = 'search/search.html'

    def get_context_data(self, **kwargs):
        '''Записываем текущие праметры, для правильной расстановки checked'''

        context = super().get_context_data(**kwargs)

        context['key'] = self.request.GET.get('key')
        context['name'] = self.request.GET.get('name')
        context['content'] = self.request.GET.get('text')
        context['tag'] = self.request.GET.get('tag')
        if self.request.GET.get('order_by') == 'date':
            context['date_filter'] = True

        count_posts = self.get_queryset_search()
        count_posts = self.exclude_del_posts(count_posts)
        count_posts = count_posts.count()
        context['count_posts'] = count_posts
        if self.request.META['QUERY_STRING'] != '': #проверяем каноничность страницы для поисковиков
            context['not_canonical'] = True
        
        context['get_request'] = self.request.META['QUERY_STRING'] #записываем адресную строку для ajax запроса
        
        return context
    
class SearchList(PostsList, SearchQuerysetMixin):
    '''Возврат найденых постов на странице поиска'''


    def get_queryset(self):
            '''Возварщает соответсвующий запрос'''
            start, end = self.get_slice(self.request, self.posts_in_page)

            tags_filter = self.get_tags_filter()

            queryset = self.get_queryset_search().exclude(tags__tag__in=tags_filter)

            queryset = self.exclude_del_posts(queryset)
          
            return queryset[start:end]

    def get(self, request, *args, **kwargs):
        data = self.get_posts()
        return HttpResponse(data)


    def post(self, request, *args, **kwargs):
        return HttpResponse('Вообще то я жду GET')
