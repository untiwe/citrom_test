from mypackage.posts_manager.posts_list import PostsList
from django.views.generic import TemplateView
from django.views.decorators.http import require_GET


# python manage.py makemigrations
# python manage.py migrate


class Index(TemplateView):
    '''Вывод шлавной страницы без постов. Посты подгружаются через ajax'''
    template_name = 'index/index.html'
    extra_context = {'title' : 'Посты с лучшими мемами и интелектуальым юмором не для всех',
        'description' : 'Можешь посмотреть что тут есть, или даже разместить свое. Но если тебя закидают минусами, не нало плакать, тебя предупреждали'}# дополнительный СТАТИЧНЫЙ context
     

     #test context_object_name = 'posts'
     #test def get_queryset(self):
     #test      return Posts.objects.prefetch_related('tags_set').all().order_by('-date_create')[:10]




class IndexNewPage(PostsList):
    '''Отображение списка постов на главной. Вся реализация в родительском классе'''
    pass


from django.http import HttpResponse
from django.views.decorators.http import require_GET


@require_GET
def robots_txt(request):
    lines = [
        "User-Agent: *",
        "Disallow: /",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")
   
