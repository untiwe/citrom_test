from mypackage.MixinClasses import SlicerMixin, GetUserMixin, GetUserStatusMixin
from django.views import View
from mymodels.models import CustomUser, Comments
from django.http import HttpResponse, JsonResponse
from mypackage.pakage import get_user_permission


class GetComments(View, SlicerMixin, GetUserMixin, GetUserStatusMixin):
    '''Возврат комментариев пользователя'''

    comments_in_page = 10
    perent = False#Нужен ли id родителя для вложенности

    def get_queryset(self):
        
        return Comments.objects.filter(post_id=self.kwargs['post_pk']).prefetch_related('commentsphotos_set', 'evaluationcomments_set').select_related(
            'post_id', 'perent_comment_id', 'user_id', 'user_id__profile').order_by('-comment_rating')


    def get_comments(self):
        user = self.get_user_session()

        # проверка что пользователь на своей странице
        out_data = {}

        # делалось для вывода в кабинете пользователся, отказался в пользу унификации out_data['avatar'] = user.profile.avatar.url
        # делалось для вывода в кабинете пользователся, отказался в пользу унификации out_data['username'] = user.username


        comments = self.get_queryset()

        if comments == None:
            return {}    
        
        comments_json_list = []

        for one_comment in comments:
            comment = {}

            comment['id'] = one_comment.pk  
            comment['avatar'] = one_comment.user_id.profile.avatar.url
            comment['username'] = one_comment.user_id.username
            comment['post_id'] = one_comment.post_id.pk
            comment['rating'] = one_comment.comment_rating
            comment['comment_text'] = one_comment.content
            if self.perent: #просто one_comment.perent_comment_id не сериализуется в JSON.
                if one_comment.perent_comment_id:    
                    comment['perent'] = str(one_comment.perent_comment_id)
                else:
                    comment['perent'] = 'False'

            if hasattr(one_comment, 'deletedcomments'):
                comment['deleted'] = True
                
            photo_model = one_comment.commentsphotos_set.all().first()
            if(photo_model):
                comment['comment_photo'] = photo_model.photo.url

            if user == False:
                comment['eval'] = 0
            else:
                comment_eval = one_comment.evaluationcomments_set.filter(  # определяем оценки комментария (да, свои комментарии тоже можно лайкать или нет)
                    user_id=user).first()
                if (comment_eval == None):
                    comment['eval'] = 0
                elif comment_eval.evaluation == True:
                    comment['eval'] = 1
                elif comment_eval.evaluation == False:
                    comment['eval'] = -1
            
            #если написаший комментарий и текущий пользователь один и тот же(или модератор), даем возможность менять комментарий
            is_access_denied, _ =  get_user_permission('change_comment', user, comment['username']) 
            if not is_access_denied:
                comment['may_change'] = True

            comments_json_list.append(comment)

        out_data['comments_list'] = comments_json_list
        return out_data

    def get(self, request, *args, **kwargs):
        return HttpResponse('Вообще то я жду POST')

    def post(self, request, *args, **kwargs):
        data = self.get_comments()

        return JsonResponse(data)