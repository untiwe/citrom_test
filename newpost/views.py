
import html
import json
from copy import deepcopy

from django.http import HttpResponse, JsonResponse
from django.views.generic import TemplateView
from mymodels.models import Posts, PostsPhotos, Tags
from mypackage.pakage import get_user_permission, get_user_session, slice_url_photo
from mypackage.compress_image import compress_image

from .forms import PhotoForm
from .package import GetPostDatamixin


# Create your views here.
class NewPost(TemplateView, GetPostDatamixin):
    '''
    Делвем загрузку страницы конструктора. По умолчанию стоит шаблон для не авторизированых пользователей. 
    Если пользователь авторизован(is_authenticated), то менаем шаблон.
    '''
    template_name = 'newpost/anonim_user.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
       
        context["post_data"] = self.get_post_data()
        
        return context
    

    def get(self, request, **kwargs):
        if self.request.user.is_authenticated:
            self.template_name = 'newpost/newpost.html' 
        
        return self.render_to_response(self.get_context_data(), **kwargs)


def SavePost(request):
    # Сохраняем пост. Приходит ajax запрос с данными, его распарсиваем
    if request.method != 'POST':
        return HttpResponse('Вообще-то, я жду POST!')

    user = get_user_session(request)

    is_access_denied, cause =  get_user_permission('create_post', user)
    if is_access_denied:
        return HttpResponse(cause)

    data = json.loads(request.POST['post'])
    name_post = data['name_post']

    post_content = data['post_content']
    
    #экранируем html в тексте поста
    for cell_content in post_content.keys():
        #if cell_content.find('_text') != -1:
            post_content[cell_content] = html.escape(post_content[cell_content])


    tags = data['tags'] + data['main_tags']
    new_post = Posts()
    new_post.author = user
    new_post.name = name_post
    new_post.content = json.dumps(post_content, ensure_ascii = False)
    new_post.save()
    new_post_id = new_post.pk  # pk и id одно и тоже

    for one_tag in tags:
        # добавлем теги в пост, по циклу
        # ОПТИМИЗАЦИЯ ЗАПОСОВ!!!!!
        # tag - вернувишиеся значение, created - булевое значение, создалось или нет
        tag, created = Tags.objects.get_or_create(tag=one_tag.strip())
        # вместо filter(tag__in=tags) ниже, собирать бы список отсюда но append просто заменяет переменную, а не вставлет новую

    for one_tag in Tags.objects.filter(tag__in=tags):
        # добавляем связи и счетчик. С get_or_create этого не сделать
        one_tag.posts.add(new_post_id)
        one_tag.count_posts += 1
        one_tag.save()

    for cell_content in post_content:
        # Ищем блоки с фоткми, и привязываем к их посту по связи foreign key
        if cell_content.find('_img') == -1:
            continue
        
        photo_src = post_content[cell_content]
        photo_src = slice_url_photo(photo_src, 'media/')
        photo = PostsPhotos.objects.get(photo=photo_src)
        photo.post_id = new_post
        photo.save()
    return HttpResponse(new_post_id)


def LoadPhoto(request):
    # имя пользователя request.user.username
    if request.method != 'POST':
        return HttpResponse('это не POST')
    form = PhotoForm(request.POST, request.FILES)
    if form.is_valid():

        form.save()
        save_form = form.instance


        save_form.photo = compress_image(save_form.photo) #преобразуем в формат webp и перезаписываем модель        
        save_form.save()
        
        print(save_form.photo.url)

        response = json.dumps([save_form.photo.url, save_form.id])
        

        # save_form.id#id последней записи
        # save_form.photo.url#url фотки
        # save_form.photo.name#имя фотки
        # еще поля тут https://docs.djangoproject.com/en/3.1/topics/files/#using-files-in-models
        return HttpResponse(response)
    else:
        return HttpResponse(form.errors.as_data())


def TagsSerch(request):
    if request.method != 'POST':
        return HttpResponse('Вообще-то, я жду POST!')
    top_tags = Tags.objects.filter(tag__istartswith=request.POST['tag']).values(
        'tag', 'count_posts').order_by('-count_posts')[:10]
    tags_dict = {}

    # Собираем словарь, уменьшаем количество текста для передачи
    for i in top_tags:
        tags_dict[i['tag']] = i['count_posts']

    return JsonResponse(tags_dict)


class NewPostPreview(TemplateView, GetPostDatamixin):
    '''Показываем предпросмотр поста'''

    template_name = 'post/post.html'
    context_object_name = 'post_data'
    extra_context = {'post_preview' : True, 'title' : 'Предпросмотр поста',}

    #DetailView есть context_object_name у него имя 'post_data' и это хорошо для вывода готовго поста. Но тут у нас нет модели из которой собирается пост, есть JSON
    #из cookie по этому, для единсва шаблона, "подгоняется" имя и контент самого поста идет в словаре 'post_data'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post_data = {}
        context["post_data"] = self.get_post_data()
        
        return context
    
def DelPostImgs(request):
    '''
    Получаем массив, удаляем фотографии. Происходит если пользователь удалил блок с фото в редакторе
    Именно массив нужен, если пост отчищается в конструкторе
    '''
    if request.method != 'POST':
        return HttpResponse('Вообще-то, я жду POST!')
    
    photo_src = request.POST.getlist('src_imgs[]')
    photo_src_list = [slice_url_photo(one_src, 'media/') for one_src in photo_src]
    PostsPhotos.objects.filter(photo__in = photo_src_list).delete()
    return HttpResponse('ok')
