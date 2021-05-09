from django.http import HttpResponse
from mymodels.models import Posts, CustomUser, EvaluationPosts, ViewsPosts, EvaluationComments, Comments
from django.db.models import F
from smalltasks.package import get_time
from django.core.cache import cache


from mypackage.pakage import get_user_permission, get_user_session


def calc_eval(eval, old_eval=None):
    '''Получаем оценку, опционально получаем существующую оценку. Возвращаем число, которе надо прибавить к счетчику'''
    if old_eval == None:
        if eval:
            return 1
        else:
            return -1
    if eval and old_eval:
        return -1
    if not eval and old_eval:
        return -2
    if eval and not old_eval:
        return +2
    if not eval and not old_eval:
        return +1


def eval_post(request):
    '''Метод для оценки постов'''
    if request.method != 'POST':
        return HttpResponse('я жду POST')

    user = get_user_session(request)

    if request.POST['command'] == 'true':
        new_eval = True
    elif request.POST['command'] == 'false':
        new_eval = False

    post = Posts.objects.select_related(
        'author').get(pk=request.POST['post_id'])

    is_access_denied, cause = get_user_permission('eval_post', user)
    if is_access_denied:
        return HttpResponse(cause)

    eval = EvaluationPosts.objects.filter(post_id=post, user_id=user).first()

    if eval == None:  # Если оценки нет, создаем и записываем
        count = calc_eval(new_eval)
        eval = EvaluationPosts(
            post_id=post, user_id=user, evaluation=new_eval)
        eval.save()
    else:  # если оценка уже есть
        count = calc_eval(new_eval, eval.evaluation)
        if eval.evaluation == new_eval:  # удаляем
            eval.delete()
        else:
            eval.evaluation = new_eval  # меняем на противоположную
            eval.save()

    # обновляем рейтинги поста и ползователя
    # считаем один раз при оценке, что бы не считать каждый раз, при запросе поста
    post.post_rating = F('post_rating') + count
    post.author.profile.user_rating = F('user_rating') + count
    post.author.save()
    post.save()
    user.save()
    cache.delete(F'rating_{post.author}')  # Удаляем рейтинг из кэша

    return HttpResponse('ok')


def eval_comment(request):
    '''Метод для оценки комментариев'''
    if request.method != 'POST':
        return HttpResponse('я жду POST')

    if request.POST['command'] == 'true':
        new_eval = True
    elif request.POST['command'] == 'false':
        new_eval = False

    comment = Comments.objects.get(pk=request.POST['comment_id'])
    user = get_user_session(request)

    is_access_denied, cause = get_user_permission('eval_comment', user)
    if is_access_denied:
        return HttpResponse(cause)

    eval = EvaluationComments.objects.filter(
        comment_id=comment, user_id=user).first()

    if eval == None:  # Если оценки нет, создаем и записываем
        count = calc_eval(new_eval)
        eval = EvaluationComments(
            comment_id=comment, user_id=user, evaluation=new_eval)
        eval.save()
    else:  # если оценка уже есть
        count = calc_eval(new_eval, eval.evaluation)
        if eval.evaluation == new_eval:  # удаляем
            eval.delete()
        else:
            eval.evaluation = new_eval  # меняем на противоположную
            eval.save()

    # обновляем рейтинг комментария и пользователя
    # считаем один раз при оценке, что бы не считать каждый раз, при запросе комментария
    comment.post_rating = F('post_rating') + count
    comment.user_id.profile.user_rating = F('user_rating') + count
    comment.user_id.profile.save()
    comment.save()
    user.save()
    cache.delete(F'rating_{comment.user_id}')  # Удаляем рейтинг из кэша

    return HttpResponse('ok')


def post_views_counter(request):
    '''Добавление посту просмотров'''
    if request.method != 'POST':
        return HttpResponse('я жду POST')
    post_id = int(request.POST.get('post_id'))

    if not request.user.is_authenticated:  # если анонимный юзер
        post_view = Posts.objects.get(id=post_id)
        post_view.views = F('views') + 1
        post_view.save()
        return HttpResponse('ok')

    
    if request.user.username == 'admin':
        return HttpResponse('ok')


    user = CustomUser.objects.get(username=request.user)
    post_id = Posts.objects.get(id=post_id)

    is_view, create = ViewsPosts.objects.get_or_create(
        post_id=post_id, user_id=user)

    if create:  # если просмотра небыло
        post_id.views = F('views') + 1
        post_id.save()
        return HttpResponse('ok')

    # Если пользователь зарегестрирован, просмотр был
    if get_time(is_view.date_update):  # Проверка на срок просмотра
        is_view.save()  # обновляем время просмотра
        post_id.views = F('views') + 1
        post_id.save()
        return HttpResponse('ok')

    return HttpResponse('ok')
