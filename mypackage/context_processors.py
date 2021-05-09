from mypackage.mycahe.user_sitebar_cahe import get_user_sitebar_cache
from versions import css_version, js_version, static_version

def set_options_views(request):
    '''Устновка опций просмотра согласно cookie'''
    context = {}
    if request.COOKIES.get('nsfw'):
        context["nsfw"] = True
    if request.COOKIES.get('gore'):
        context["gore"] = True
    if request.COOKIES.get('politic'):
        context["politic"] = True
    if request.COOKIES.get('hide_view'):
        context["hide_view"] = True
    if request.COOKIES.get('is_18_age'):
        context["is_18_age"] = True

    context["user_rating"], context["posts_count"], context["user_avatar"], context["user_new_message"] = get_user_sitebar_cache(request)

    #устанавлоиваем версии статичных файлов, для обновления со стороны пользвателя
    context["css_version"] = css_version
    context["js_version"] = js_version
    context["static_version"] = static_version

    return context

    
    
