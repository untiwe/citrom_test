from mymodels.models import CustomUser


class SlicerMixin():
    '''Миксин для подсчета среза, вывода данных на страницу'''

    def get_slice(self, request, size_page):
        '''Расчитываем велечину среза, принимаем request и велечину на одну страницу'''
        if request.method == 'GET':
            num_page = int(request.GET.get('page'))
        elif request.method == 'POST':
            num_page = int(request.POST.get('page'))

        end = num_page * size_page
        start = end - size_page
        return start, end

class GetUserMixin():
    '''Получем модель текщего пользователя или False'''

    def get_user_session(self):
        '''определяем пользователя'''
        user = False 

        if self.request.user.is_authenticated:  # если это юзер
           user = CustomUser.objects.get(username=self.request.user)
        
        return user

class GetBoolThisUserMixin():
    '''Класс для проверки, пользователя. '''

    def get_bool_this_user(self):
        '''Сверка "username" из request.user и параметра "username" из пришедшего url. Если пользователь зашел на свою стрицу - true, если на чужую false '''
        if str(self.request.user) == str(self.kwargs['username']):
            return True
        else:
            return False

class ExcludeDelPostsMixin():
    '''Класс для добавления в фильтрацию удаленых постов, конкретного пользователя'''

    def exclude_del_posts(self, queryset, user = False):
        '''Принимаем фитр постов и добавляем в него исключение удаленных. Если получили модель пользователя, его удаленные посты не исключаем'''
        if user == False:#если не прислали модель пользователя прсто фильтруем все удаленные посты
            return queryset.exclude(deletedposts__post_deleted__gte = 1)

        #вот если мы получили модель пользователя...
        #помним, что в таблице author поста, это просто его id. По этому сключаем удаленные посты у которых author больше, а потом у которых меньше нашего автора.
        queryset = queryset.exclude(deletedposts__post_deleted__author__gt = user)
        queryset = queryset.exclude(deletedposts__post_deleted__author__lt = user)
        return queryset

class GetUserStatusMixin():
    '''Класс для узнавания, статуса пользователя'''

    def get_user_status(self, user, author = False):
        '''Получает пользователя и возвращает его статус. Если получила author и author == user вернет статус модератора'''
        if user == False:
            return 100 #возвращаем статус обычного пользователя

        if user.username == author:
            return 101
        
        return user.group

class GetRequsestUserStatusMixin():
    '''Класс для узнавания, статуса пользователя. который делает запрос'''

    def get_request_user_status(self, request_user, user = False):
        '''Получает модель пользователя и возвращает его статус. Если получила user и request_user == user вернет статус модератора'''
        if request_user == False:
            return 100 #возвращаем статус обычного пользователя

        if request_user == user:
            return 101
        
        return request_user.group