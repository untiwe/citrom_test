class SetDefaulCookie:
    '''Класс установки стандартых куки, делался для исследования MIDDLEWARE. В данный момент (25.02.21) отключен за ненадобностью'''
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        response = self.get_response(request)
        
        # response.set_cookie('testName', 'testvalue')
        # print(request.COOKIES)

        return response