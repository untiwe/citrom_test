from django.core.mail import EmailMessage


def send_mail():
    '''Отправлячем уведомление на мою почту'''
    

    email = EmailMessage(
        subject = 'Новое сообщение',
        body = F'Привет!У нас там новое сообщение',
        from_email = 'info@citrom.ru',
        to = ("untiwe@gmail.com",)
    )
    
    email.send()