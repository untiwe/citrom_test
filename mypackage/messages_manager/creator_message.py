import json
from django.core.cache import cache
from mymodels.models import CustomUser, Messages, Posts


def send_new_comment(comment):
    '''Создаем сообщение при новом комментарии. Шлется автору поста, если ответ на комментарий, шлется автору комментария'''
    
    save_comment = {}
   
    save_comment['this_comment_id'] = comment.pk  
    save_comment['this_comment_author'] = comment.user_id.username

    perent_post = Posts.objects.get(comments__pk = comment.pk)
    save_comment['post_id'] = perent_post.id
    save_comment['post_name'] = perent_post.name
    save_comment['post_author'] = perent_post.author.username

    if save_comment['post_author'] == save_comment['this_comment_author']:#Если пользователь оставил комментарий под свои постом, ничего не делаем
        return

    save_comment['comment_text'] = comment.content
    photo_model = comment.commentsphotos_set.all().first()
    if(photo_model):
        save_comment['comment_photo'] = photo_model.photo.url

    if comment.perent_comment_id: #просто one_comment.perent_comment_id не сериализуется в JSON.
        save_comment['perent_comment_id'] = comment.perent_comment_id.id
        save_comment['perent_comment_author'] = comment.perent_comment_id.user_id.username
        if save_comment['perent_comment_author'] == save_comment['this_comment_author']:#Если пользователь ответил на свой комментарий, ничего не делаем
            return
        #определяем тип сообщения и пользователя для связи        
        type = 'answer_comment'
        user = CustomUser.objects.get(username=save_comment['perent_comment_author'])
    else:
        type = 'comment_post'
        user = CustomUser.objects.get(username=save_comment['post_author'])
    

    
    save_comment = json.dumps(save_comment, ensure_ascii = False)
    mess = Messages(user_id = user, type = type, text = save_comment)
    mess.save()
    user_new_message(user)


def send_del_post(initiator_user, post, cause):
    '''Уведомляем пользователя об удалении поста. Даже если он сам это сделал'''
    
    type = 'post_delete_moderator'
    if post.author.username == initiator_user.username:
        type = 'post_delete_author'

    data_message = {}
    data_message['post_id'] = post.id
    data_message['post_name'] = post.name
    data_message['post_author'] = post.author.username
    data_message['who_deleted_name'] = initiator_user.username
    data_message['who_deleted_id'] = initiator_user.id
    data_message['cause'] = cause
    data_message = json.dumps(data_message, ensure_ascii = False)

    whom_message = CustomUser.objects.get(username = post.author.username)


    mess = Messages(user_id = whom_message, type = type, text = data_message)
    mess.save()
    user_new_message(whom_message)
    

def user_new_message(user_model):
    '''Ставим ответку о непрочитаных сообщениях'''
    user_model.profile.messages_count = True
    cache.delete(F'new_message_{user_model}')
    user_model.save()


def send_del_comment(initiator_user, comment, cause):
    '''Уведомляем пользователя об удалении комментария. Даже если он сам это сделал'''
    
    c = comment.post_id.author

    type = 'comment_delete_moderator'
    if comment.user_id == initiator_user:
        type = 'comment_delete_author'

    
    data_message = {}
    if(comment.perent_comment_id):
        perent = comment.perent_comment_id
        data_message['perent_comment_id'] = perent.id
        data_message['perent_comment_author_id'] = perent.user_id.id
        data_message['perent_comment_author_name'] = perent.user_id.username
 
    post = comment.post_id
    data_message['comment_post_id'] = post.id
    data_message['comment_post_name'] = post.name

    data_message['comment_author_id'] = comment.user_id.id
    data_message['comment_author_name'] = comment.user_id.username

    data_message['who_deleted_name'] = initiator_user.username
    data_message['who_deleted_id'] = initiator_user.id
    data_message['cause'] = cause
    data_message = json.dumps(data_message, ensure_ascii = False)

    whom_message = CustomUser.objects.get(username = comment.user_id.username)


    mess = Messages(user_id = whom_message, type = type, text = data_message)
    mess.save()
    
    user_new_message(whom_message)

    





