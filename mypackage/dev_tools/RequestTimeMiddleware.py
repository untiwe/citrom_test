import time

class RequestTimeMiddleware:
    '''Смотрим время выполнения запроса. Источник кода https://habr.com/ru/company/barsgroup/blog/523068/'''

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        timestamp = time.monotonic()

        response = self.get_response(request)

        print(
            f'Продолжительность запроса {request.path} - '
            f'{time.monotonic() - timestamp:.3f} сек.'
        )

        return response

