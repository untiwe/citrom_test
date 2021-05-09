from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.detail import DetailView
from mymodels.models import Comments, CommentsPhotos, CustomUser, Posts
from mypackage.comments_view.comments_list import GetComments
from mypackage.messages_manager.creator_message import send_new_comment
from mypackage.pakage import get_user_session, get_user_permission
from mypackage.posts_manager.posts_list import GetUserMixin
import html

class Post(DetailView, GetUserMixin):
    '''Вывод страницы с постом'''
    model = Posts
    template_name = 'post/post.html'
    pk_url_kwarg = 'post_pk'
    context_object_name = 'post_data'

    def get_queryset(self):
        return Posts.objects.select_related('author').prefetch_related(
            'evaluationposts_set', 'tags_set', 'comments_set').filter(pk=self.kwargs['post_pk'])
        

    def get_context_data(self, **kwargs):
        # Оптимизация запостов!!!!!!!!!!!!!!

        context = super().get_context_data(**kwargs)
        # через get_queryset, get запрос не сделать, а он нужен что бы поправить content

        user = self.get_user_session()

        # использовалось для шаблона comments = Comments.objects.filter(
            #post_id=self.kwargs['post_pk']).select_related('perent_comment_id', 'user_id', 'post_id').prefetch_related('commentsphotos_set', 'comments_set').order_by('-comment_rating')
        # использовалось для шаблона context['comments'] = comments
       
        context['comments_count'] = Comments.objects.filter(post_id=self.kwargs['post_pk']).count()


        # Большая часть контета поста реализована функцией get_content_dict в модели. Для универсального использования шаблона в др. приложениях
        # анализ запроса print(comments.explain())
        
        #узнаем пользователя и его оценку поста
        post = self.get_queryset()[0]
        if not user:
            context['eval'] = 0
        post_eval = post.evaluationposts_set.filter(user_id=user).first()
        if (post_eval == None):
            context['eval'] = 0
        elif post_eval.evaluation == True:
            context['eval'] = 1
        elif post_eval.evaluation == False:
            context['eval'] = -1

        # Даем право менять пост, если это автор или модератор
        is_access_denied, _ =  get_user_permission('change_post', user, post.author.username) 
        if not is_access_denied:
            context['may_change'] = True

        return context

    def get(self, request, *args, **kwargs):
        '''Проверяем ниличе поста и перенаправляем пользователя, если пост удален или нет прав доступа'''
       
        post = get_object_or_404(Posts, pk=self.kwargs['post_pk'])
        user = self.get_user_session()
        
        if hasattr(post, 'deletedposts'):
            if user:
                if post.author.username == user.username or user.group == 101:
                    pass
                else:
                    return redirect('/')
            else:
                return redirect('/')


        return super().get(request, *args, **kwargs)

class GetCommentsPost(GetComments):
    '''Возвращаем JSON с комментариями к посту'''
    perent = True
    

def CommentPhoto(request):
    '''Сохранение фото комментария'''
    if request.method != 'POST':
        return HttpResponse('это не POST')
    if not request.user.is_authenticated:
        return HttpResponse('error:Только зарегестированые пользователи могут загружать фотографии')

    new_photo = CommentsPhotos(photo=request.FILES['photo'])
    new_photo.save()
    return JsonResponse([new_photo.photo.url, new_photo.pk], safe=False)
    # test return JsonResponse(["/media/comments/2021/01/09/0_1PDvJxy.png", 20],safe=False)


def NewComment(request):
    '''Сохраняем новый комментарий'''
    if request.method != 'POST':
        return HttpResponse('это не POST')
    
    user = get_user_session(request)
    is_access_denied, cause =  get_user_permission('create_post', user)
    if is_access_denied:
        return HttpResponse(cause)

    comment = Comments()
    comment.post_id = Posts.objects.get(pk=request.POST['post_id'])
    if 'perent_comment_id' in request.POST:
        # если у комментария есть родитель(отвечают кому то) пишем
        comment.perent_comment_id = Comments.objects.get(
            pk=request.POST['perent_comment_id'])
    comment.content = html.escape(request.POST['content']) #экранируем HTML
    comment.user_id = CustomUser.objects.get(username=request.user.username)
    comment.save()
    if 'photo_id' in request.POST:  # привязываем фотку к коментарию
        comment_photo = CommentsPhotos.objects.get(pk=request.POST['photo_id'])
        comment_photo.сomment_id = comment
        comment_photo.save()
    
    send_new_comment(comment)#Создаем уведомление о комментарии

    return HttpResponse('ok')
