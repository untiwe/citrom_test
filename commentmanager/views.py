from django.http.response import HttpResponse
from mymodels.models import Comments, DeletedComments
from django.views.generic.base import View
from mypackage.MixinClasses import GetUserMixin, GetUserStatusMixin
from mypackage.messages_manager.creator_message import send_del_comment
from mypackage.pakage import get_user_permission

# Create your views here.


class CommentDelete(View, GetUserMixin):
    '''Класс удаления комментариев'''

    def get(self, request, *args, **kwargs):
        return HttpResponse('Вообще то я жду POST')

    def post(self, request, *args, **kwargs):

        user = self.get_user_session()
        comment = Comments.objects.get(id = self.request.POST.get('comment_id'))
        cause = self.request.POST.get('cause')


        is_access_denied, refusals_cause =  get_user_permission('change_comment', user, comment.user_id.username)
        if is_access_denied:
            return HttpResponse(refusals_cause)

        

        if hasattr(comment, 'deletedcomments'):
            return HttpResponse('error:Этот комментарий уже удален')
        
        del_comment = DeletedComments(comment_deleted=comment, user_deleted = user, cause = cause)
        del_comment.save()

        send_del_comment(user, comment, cause)#отправляем сообщение об удалении комментария

        return HttpResponse('ok')
    
    def get_resolution_user(self, user, comment):
        '''Получаем модель пользователя и поста. Возвращаем группу пользователя, или возвращаем false если у пользователя нет доступа'''
        
        if user == False:
            return False

        if user.group == 101:
            return 101
        
        if comment.user_id.username == user.username:
            return 100
        
        return False
