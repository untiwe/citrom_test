from django.core.cache import cache
from mypackage.pakage import get_user_session
from mymodels.models import Posts, CustomUser


def get_user_sitebar_cache(request):
    '''Устанавливаем (если надо) и возвращаем статитику пользователя для sitebara, если пользователь не авторизован, возврашаем None'''
    user = get_user_session(request)
    if user == False:
        return None, None, None, None

    #Если пользователь заходит на страницу с сообщениями, удаляем пометку о новых сообщени в кеше 
    if request.method == 'GET' and request.path.find('/messages/') == 0:
        user.profile.messages_count = False
        cache.delete(F'new_message_{user}')
        user.save()

    rating, count, avatar, new_message = get_user_cache(user, 'rating', 'posts_count', 'avatar', 'new_message')
    return rating, count, avatar, new_message

def get_user_cache(user : CustomUser, *keys):
    '''
    Устанавливаем (если надо) и возвращаем статитику пользователя, принимаем объект пользователя из БД
    Если нет keys вернут все значения в порядке ключей: rating, posts_count, avatar, new_message
    Если есть несколько ключей, вернет тот порядок и количество, в соответсвии с которым они пришли
    например: 'avatar', 'posts_count'

    '''
    key_rating = F'rating_{user}'
    key_posts_count = F'posts_count_{user}'
    key_user_avatar = F'avatar_{user}'
    key_new_message = F'new_message_{user}'

    default_keys_list = ['rating', 'posts_count', 'avatar', 'new_message']
    out_list = []

    if cache.get(key_rating) == None:
        user_rating = user.profile.user_rating
        cache.set(key_rating, user_rating)
    if cache.get(key_posts_count) == None:
        posts_count = Posts.objects.filter(author=user).count()
        cache.set(key_posts_count, posts_count)
    if cache.get(key_user_avatar) == None:
        user_avatar = user.profile.avatar.url
        cache.set(key_user_avatar, user_avatar)
    if cache.get(key_new_message) == None:
        new_message = user.profile.messages_count
        cache.set(key_new_message, new_message)

    if len(keys) == 0:#если аргументов нет, возвращаем всё
        for key in default_keys_list:
            out_list.append(cache.get(F'{key}_{user}'))

    if len(keys) == 1:#если аргумент один, возвращаем его(вне массива)
        return cache.get(F'{keys[0]}_{user}')


    for key in keys:#Если аргументов несколько, возвращаем их массив
        out_list.append(cache.get(F'{key}_{user}'))
    
    return out_list

    
