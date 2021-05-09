from PIL import Image
from citrom.settings import BASE_DIR, DEBUG # берем адрес корня проекта из settings
import os
import random
import string

def generate_random_string(length):
    '''генерируем случайный набор букв'''
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


def compress_image(image):

    

    # if DEBUG:#если на тестовом сервере, ничего не делаем
    #     return image.url.replace('/media/','')
    
    # filepath =file.url.replace('/','\\')# для винды
    filepath = image.url #для сервера
    
    picture = Image.open(str(BASE_DIR) + filepath).convert('RGB')
    print(str(BASE_DIR) + filepath)

    photo_name_end = generate_random_string(6)

    photo_url = (str(BASE_DIR) + filepath).split('.')[:-1]
    photo_url = '.'.join(photo_url)
    photo_url = f'{photo_url}{photo_name_end}.webp'
    picture.save(photo_url, 'webp')

    
    #удаляем старую картинку
    os.remove(str(BASE_DIR) + filepath)

    #формируем путь нового файла для модели
    new_filepach = image.url.split('.')[0]



    new_filepach = new_filepach.replace('/media/','')
    new_filepach = f'{new_filepach}{photo_name_end}.webp'
    with open("file.txt", "w") as f:

        f.write(f'(str(BASE_DIR) + filepath) = {(str(BASE_DIR) + filepath)}')
        f.write(f'photo_url = {photo_url}')
        f.write(f'new_filepach = {new_filepach}')
        # /var/www/u1164481/data/www/citrom.ru/media/posts/2021/04/27/image_vyAuJzH.png
        # /var/www/u1164481/data/www/citrom.webp
    
    return new_filepach


    # сжатие картинки через уменьшение размера и качеста
    # picture = picture.resize((160,300),Image.ANTIALIAS)
    # picture.save(str(BASE_DIR) + filepath, 
    #              optimize = True, 
    #              quality = 10)