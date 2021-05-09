import json


class GetPostDatamixin():
    '''Класс для флрмирования значений поста из cookies нужно для предпросмотра поста и сохранения значений конструктора'''

    def get_post_data(self):
        '''берем из запроса cookeies - raw_user_post и формируем словарь post_data'''
        post_data = {}
        post_data['author'] = self.request.user
        post_data['post_rating'] = 0

        return post_data
        #остальное использовалось из cookie и использовалось в шаблое. Теперь эти данные соббирает и грузит JS из licalstorage 
        main_tags_dict = {'nsfw', 'жесть', 'политика', 'мое'}
        post_data = {}
        input_data = self.request.COOKIES.get('raw_user_post')
        if input_data == None:
            return
        input_data = json.loads(input_data)

        post_data['name'] = input_data.get('name_post')
        if post_data['name'] == None:
            post_data['name'] = ' '
        
        #сборка обычных тегов для конструктора
        post_data['tags'] = input_data.get('tags')
        #сборка главных тегов для конструктора
        post_data['main_tags'] = input_data.get('main_tags')
        #сборка всех тегов для страницы предпросмотра поста
        post_data['all_tags'] =  input_data.get('main_tags') + input_data.get('tags')

        post_data['post_content'] = input_data.get('post_content') 
        post_data['raw_post_content'] = input_data.get('raw_post_content') 
        
        post_data['author'] = self.request.user
        post_data['post_rating'] = 0
        p = post_data['raw_post_content']

        return post_data

