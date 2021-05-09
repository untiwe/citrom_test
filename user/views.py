from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic.detail import DetailView
from mymodels.models import (Comments, CustomUser, EvaluationPosts, Posts,
                             Profile, SubTags, Tags)
from mypackage.comments_view.comments_list import GetComments
from mypackage.MixinClasses import (GetBoolThisUserMixin,
                                    GetRequsestUserStatusMixin, GetUserMixin)
from mypackage.mycahe.user_sitebar_cahe import get_user_cache
from mypackage.posts_manager.posts_list import PostsList

# смена пароля через классы https://www.youtube.com/watch?v=cBYAa_kI_Bk


class UserView(DetailView, GetUserMixin, GetRequsestUserStatusMixin):
    model = CustomUser
    template_name = 'user/user.html'
    context_object_name = 'user'

    def get_object(self):
        return get_object_or_404(CustomUser, username=self.kwargs['username'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.get_object()
        request_user = self.get_user_session()
        #Счетчики лайков/дислайков пользователя
        context['liked_posts'] = EvaluationPosts.objects.filter(user_id=user, evaluation=True).count()
        context['disliked_posts'] = EvaluationPosts.objects.filter(user_id=user, evaluation=False).count()
        

        # добавляем дату рождения одним запросом, что бы не обращаться несколько раз в шаблоне
        context['profile'] = Profile.objects.get(user_base=user)
        tags_list = SubTags.objects.filter(user_id=user)
        # выбираем подписаные/заблоченые теги
        sub_tags_list = set()
        block_tags_list = set()
        for tag in tags_list:
            if tag.status == True:
                sub_tags_list.add(tag.tag_id)
            if tag.status == False:
                block_tags_list.add(tag.tag_id)

        context['sub_tags_list'] = sub_tags_list
        context['block_tags_list'] = block_tags_list

        context['this_user'] = self.get_request_user_status(request_user, user) > 100


        context['is_user_rating'] = get_user_cache(user, 'rating')
        context['is_user_posts_count'] = get_user_cache(user, 'posts_count')
        context['is_user_avatar'] = get_user_cache(user, 'avatar')
        

        return context
    


def help_serch_tags(request, username):
    if request.method != 'POST':
        return HttpResponse('я жду POST')

    user = CustomUser.objects.get(username=request.user)
    tag = request.POST.get('tag').lower()
    tags_list = Tags.objects.filter(tag__istartswith=tag).values('tag').order_by(
        '-count_posts')[:10].values_list('tag', flat=True)  # удобен при получении одиночных значений
    return JsonResponse(list(tags_list), safe=False)


class GetPosts(PostsList, GetBoolThisUserMixin, GetRequsestUserStatusMixin):
    '''Вывод постов пользователя'''

    def get_queryset(self):

        user = CustomUser.objects.get(
            username=self.kwargs['username'])
        request_user = self.get_user_session()
        start, end = self.get_slice(self.request, self.posts_in_page)

        if self.get_request_user_status(request_user, user) > 100:
            tags_filter = []  # не применяем фильтры, если пользователь на своей странице, или это модератор
        else:
            tags_filter = self.get_tags_filter()

        

        query_posts = Posts.objects.select_related('author').prefetch_related(
            'evaluationposts_set', 'tags_set', 'comments_set').filter(author=user).exclude(tags__tag__in=tags_filter).order_by('-pk')

        if user != False and self.get_request_user_status(request_user, user) == 101:#если пользователь на ствоей странице, или модератор показываем его удаленные посты
            query_posts = self.exclude_del_posts(query_posts, user)
        else:
            query_posts = self.exclude_del_posts(query_posts)

        return query_posts[start:end]

class LikePosts(PostsList, GetBoolThisUserMixin, GetRequsestUserStatusMixin):
    '''Возврат понравившихся постов'''

    post_status = True

    def get_queryset(self):
        user = CustomUser.objects.get(username=self.request.user.username)

        user = CustomUser.objects.get(
            username=self.kwargs['username'])
        request_user = self.get_user_session()

        user_staus = self.get_request_user_status(request_user, user)
        # проверка группы польщователя, если меньше 100 ничего не возвращаем
        if user_staus < 101:
            return None

        start, end = self.get_slice(self.request, self.posts_in_page)

        query_posts = Posts.objects.select_related('author').prefetch_related('evaluationposts_set', 'tags_set', 'comments_set')
        query_posts = query_posts.filter(evaluationposts__user_id=user, evaluationposts__evaluation=self.post_status)

        if user != False and user_staus == 101 :#если пользователь на ствоей странице, показываем его удаленные посты
            query_posts = self.exclude_del_posts(query_posts, user)
        elif user_staus > 101: #если на странцие модератор, не убираем удаленые посты
            pass
        else: #убираем все удаленные посты, но для этого группа пользщователя должна быть 100 или меньше, а это проверяется выше
            query_posts = self.exclude_del_posts(query_posts)

        query_posts = query_posts.order_by('-pk')
        return query_posts[start:end]


class DislikePosts(LikePosts):
    '''Возврат не понравившихся постов'''

    post_status = False


class GetCommentsUser(GetComments, GetRequsestUserStatusMixin):
    '''Возврат список комментариев пользователя'''

    def get_queryset(self):


        user = CustomUser.objects.get(
            username=self.kwargs['username'])

        request_user = self.get_user_session()

        user_staus = self.get_request_user_status(request_user, user)

        if user_staus < 101:
            return None
        start, end = self.get_slice(self.request, self.comments_in_page)

        q = Comments.objects.prefetch_related('commentsphotos_set', 'evaluationcomments_set').select_related(
            'post_id', 'perent_comment_id', 'user_id', 'user_id__profile').filter(
            user_id=user).exclude(deletedcomments__comment_deleted__gt = 1).order_by('-date_create')[start:end]


        return q
