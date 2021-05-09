from django.http.response import HttpResponse
from mymodels.models import Posts, DeletedPosts
from django.views.generic.base import View
from mypackage.MixinClasses import GetUserMixin
from mypackage.messages_manager.creator_message import send_del_post
from mypackage.pakage import get_user_permission


# Create your views here.


class PostDelete(View, GetUserMixin):
    '''Класс удаления постов'''

    def get(self, request, *args, **kwargs):
        return HttpResponse('Вообще то я жду POST')

    def post(self, request, *args, **kwargs):

        user = self.get_user_session()
        post = Posts.objects.get(id = self.request.POST.get('post_id'))
        cause = self.request.POST.get('cause')


        is_access_denied, refusals_cause =  get_user_permission('change_post', user, post.author.username)
        if is_access_denied:
            return HttpResponse(refusals_cause)

        
        if hasattr(post, 'deletedposts'):
            return HttpResponse('error:Этот пост уже удален')
        
        del_post = DeletedPosts(post_deleted=post, user_deleted = user, cause = cause)
        del_post.save()

        send_del_post(user, post, cause)#отправляем сообщение об удалении поста

        return HttpResponse('ok')
    
    def get_resolution_user(self, user, post):
        '''Получаем модель пользователя и поста. Возвращаем группу пользователя, или возвращаем false если у пользователя нет доступа'''
        
        if user == False:
            return False

        if user.group == 101:
            return 101
        if post.author.username == user.username:
            return 100
        
        return False
