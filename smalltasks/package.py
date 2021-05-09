from datetime import datetime

#возможе не корректный расчет т.к. datetime.now = мето на компьютере, а приходит время из моели, UTC+0
def get_time(date_view):#получет дату
    '''
    Расчитываем разницу между прошлым просмотром и текущим, 
    возвращаем True если больше определенного кол-ва иначе False
    '''
    limit = 64800 #64800 секунд это 18 часов

    date_view = date_view.timestamp()
    date_now = datetime.now().timestamp()
    time_def =  int(date_now) - int(date_view)
    if time_def > limit:
        return True
        
    return False