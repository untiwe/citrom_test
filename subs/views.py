from django.views.generic import ListView
from mymodels.models import Posts
from mypackage.posts_manager.posts_list import PostsList
from django.views.generic import TemplateView
from mypackage.MixinClasses import GetUserMixin

# python manage.py makemigrations
# python manage.py migrate


class Subs(TemplateView, GetUserMixin):
     '''Вывод страницы с продписками без постов. Посты подгружаются через ajax'''
     template_name = 'subs/subs.html'

     def get_context_data(self, **kwargs):
          '''Проеделяем аутентификацию и наличие подписок'''
          context = super().get_context_data(**kwargs)
          user = self.get_user_session()
          if user == False:
               context['is_user_subs'] = -1
               return context
          
          context['is_user_subs'] = user.subtags_set.filter(status=True).count()
          return context
          


class SubsNewPage(PostsList):

     '''Отображение списка постов по подписаным тегам'''

     def get_queryset(self):
          '''Возварщает соответсвующий запрос'''
          start, end = self.get_slice(self.request, self.posts_in_page)
          user = self.get_user_session()
          list_views_posts = self.get_list_views_posts()

          tags = user.subtags_set.filter(status=True)

          tags_list = [i.tag_id for i in tags]

          query_posts = Posts.objects.select_related('author').prefetch_related(
               'evaluationposts_set', 'tags_set', 'comments_set').filter(tags__tag__in=tags_list).exclude(id__in=list_views_posts)

          query_posts = self.exclude_del_posts(query_posts)
          query_posts = query_posts.order_by('-pk')
          
          return query_posts[start:end]
     
     