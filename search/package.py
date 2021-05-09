from django.db.models import Q
from mymodels.models import Tags, Posts


class SearchQuerysetMixin():
    '''Миксин для сборки запроса исходя из настроек поиска'''

    def get_tags_filter_Search(self):
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


    def get_queryset_search(self):
            '''Определяем какие данные пришли из get и собираем запрос или возвращаем количество постов'''

            request = self.request

            tags_filter = self.get_tags_filter_Search()

            key = request.GET.get('key')
            name = request.GET.get('name')
            content = request.GET.get('text')
            tag = request.GET.get('tag')


            if request.GET.get('order_by'):
                order = 'date_create'
            else:
                order = 'post_rating'

            if not name and not content and not tag and not key:
                # Если нет параметров, просто вернем как index
                    return Posts.objects.all().exclude(tags__tag__in=tags_filter)


            if not name and not content and not tag and key:
                # если нет параметров, но есть ключенвое слово. Скорее всего перешли из поиска в шапке. Тогда делаем все 3 фильтра
                return Posts.objects.prefetch_related('tags_set').filter(
                    Q(name__icontains=key) | Q(content__icontains=key) | Q(tags__tag__icontains=key)).exclude(tags__tag__in=tags_filter).order_by('-post_rating').distinct()
            

            filters = Q()

            if name:
                filters |= Q(name__icontains=key)
            if content:
                filters |= Q(content__icontains=key)
            if tag:
                filters |= Q(tags__tag__icontains=key)

            if request.GET.get('order_by') == 'date':
                order = '-id'
            else:
                order = 'post_rating'
            
            # Ну чтож присаживайся. Я расскажу тебе много новго.
            # Если делать класс Q cо связаными таблицами, django добавлет в запрос JOIN
            # Он нужен для работы со связаными таблицами, но в тоже время немного ломает их и запрос может прийти как из основной таблицы, так и из связанной
            # Тут не указан наш пример, но рассказано про нашу проблему https://habr.com/ru/post/448072/
            # Она решается изменением SELECT на SELECT DISTINCT в запросе, но мы же формируем его не напрямую, а через функции
            # Для этого есть метод https://docs.djangoproject.com/en/3.1/ref/models/querysets/#distinct, но он рабоатет с треьего раза
            # По началу мне выдавало "DISTINCT ON fields is not supported by this database backend" но в после очередного удаления --> перезагрузки --> вставки --> перезагрузки, он заработал.
            # Что странно, ведь в интренетах пишут что SQLite и MySQL не поддерживаются.
            # Пока работает, и ладно, но я так понимааю, порядок работает не корректно. Сначалда упорядочивает основную таблицу, потом связанные и только потом соеденяет их а не наоборот

            
            return Posts.objects.filter(filters).exclude(tags__tag__in=tags_filter).order_by(order).distinct()
        