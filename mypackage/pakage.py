#Файл дл хранения различный вспомогательных функций
from mymodels.models import CustomUser


def get_user_session(request):
   '''Определяем пользователя или возвращаем False, аналог класса GetUserMixin'''
   user = False 

   if request.user.is_authenticated:  # если это юзер
      user = CustomUser.objects.get(username=request.user)
   
   return user

# def get_user_session(request):
#        '''Определяем пользователя или возвращаем False, аналог класса GetUserMixin'''
#    user = False 

#    if request.user.is_authenticated:  # если это юзер
#       user = CustomUser.objects.get(username=request.user)
   
#    return user




#действия:
#eval_post
#eval_comment
#create_post
#create_comment
#change_post
#change_comment
#группы:
#is_superuser           |админимстратор, допускается в админку
#102 - moderator        |модератор можеть удалять все комментарии посты и комментарии
#101 - author           |автор может удалять свои посыт и коментарии
#100 - standart_user    |просто пользователь
#99 - user_ban_lvl_1    |бан 1-го уровня нельзя комментировать и делать посты
#98 - user_ban_lvl_2    |бан 2-го уровня как 1-ый + нельзя ставить оценки
#80 - not_authenticated |не авторизованый пользователь


roots_users = {102 : {'eval_post' :    [False, ''], 
                      'eval_comment':  [False, ''], 
                      'create_post' :  [False, ''], 
                      'create_comment':[False, ''],
                      'change_post':   [False, ''],
                      'change_comment':[False, ''],
                      },
               101 : {'eval_post' :    [False, ''], 
                      'eval_comment':  [False, ''], 
                      'create_post' :  [False, ''], 
                      'create_comment':[False, ''],
                      'change_post':   [False, ''],
                      'change_comment':[False, ''],
                      },
               100 : {'eval_post' :    [False, ''], 
                      'eval_comment':  [False, ''], 
                      'create_post' :  [False, ''], 
                      'create_comment':[False, ''],
                      'change_post':   [True, 'error:Это не ваш пост'],
                      'change_comment':[True, 'error:Это не ваш комментарий'],
                      },
                99 : {'eval_post' :    [False, ''], 
                      'eval_comment':  [False, ''], 
                      'create_post' :  [True, 'error:Вы пока не можете этого сделать'], 
                      'create_comment':[True, 'error:Вы пока не можете этого сделать'],
                      'change_post':   [True, 'error:Это не ваш пост'],
                      'change_comment':[True, 'error:Это не ваш комментарий'],
                      },
                98 : {'eval_post' :    [True, 'error:Вы пока не можете этого сделать'], 
                      'eval_comment':  [True, 'error:Вы пока не можете этого сделать'], 
                      'create_post' :  [True, 'error:Вы пока не можете этого сделать'], 
                      'create_comment':[True, 'error:Вы пока не можете этого сделать'],
                      'change_post':   [True, 'error:Это не ваш пост'],
                      'change_comment':[True, 'error:Это не ваш комментарий'],
                      },
                80 : {'eval_post' :    [True, 'error:Только зарегестированные пользователи могут это сделать'], 
                      'eval_comment':  [True, 'error:Только зарегестированные пользователи могут это сделать'], 
                      'create_post' :  [True, 'error:Только зарегестированные пользователи могут это сделать'], 
                      'create_comment':[True, 'error:Только зарегестированные пользователи могут это сделать'],
                      'change_post':   [True, 'error:Только зарегестированные пользователи могут это сделать'],
                      'change_comment':[True, 'error:Только зарегестированные пользователи могут это сделать'],
                      }
}


def get_user_permission(action : str, request_user : CustomUser, target_user : str = False ):
      '''
      Получаем запрос действие и модель пользователя. 

      Если действие разрешено, возвращаем [False, '']
      Если действие запрещено, возвращаем [True, 'error:Причина запрета']

      Если 3-им аргументом пришло имя пользователя и оно == request_user.unsername. Но возврщаются расширенные права.
      Как у модератора. Эта проверка используется что бы ползователь мог удалять свои посты/комментарии
      Пример: [False, ''] хоть вторая часть массива не нужна, формат сохранен для универсальности
      
      '''
      if request_user == False:
            return roots_users[80][action]
      
      if request_user.is_superuser:
             return [False, '']

      if request_user.username == target_user:
            return roots_users[101][action]
          
      
      return roots_users[request_user.group][action]


def slice_url_photo(raw_url: str, slise_key : str):
      '''
      Получаем строку с полным url. "http..."
      Обрезаем строку вместе с ключем и возвращаем ее.
      Нужно для формирования строки, для поиска фото по ImageField
      '''

      index_slise = raw_url.find(slise_key) + len(slise_key)
      photo_src = raw_url[index_slise:]
      return photo_src