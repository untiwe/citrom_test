import string
import secrets
import random

#пример из документации https://docs.python.org/3/library/secrets.html
def gen_new_password():
    '''Функция возвращает пароль 6-10 символов'''
    alphabet = string.ascii_letters + string.digits

    while True:
        range_password = random.randint(6, 10)
        password = ''.join(secrets.choice(alphabet) for i in range(range_password))
        if (any(c.islower() for c in password)
                and any(c.isupper() for c in password)
                and sum(c.isdigit() for c in password) >= 3):
            break

    return password