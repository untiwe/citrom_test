from django import template
import re

register = template.Library()

#       let re = /([^\"=]{2}|^)((https?|ftp):\/\/\S+[^\s.,> )\];'\"!?])/g; 
#       let subst = '$1<a href="$2" target="_blank">$2</a>'; 
#       let withlink = text.replace(re, subst);


@register.simple_tag
def wrap_text(text):
    '''Функция принмает текст поста, и его с оформленными ссылками. ссылка --> <a href="ссылка">cссылка/a>'''

    ready_links = []

    regex = "((http|https|ftp):\/\/\S+)"
    result = re.findall(regex, text)
    #если ссылка кортеж типа ('https://search.google.com/', 'https')
    #2-ая егшо часть не нужна но я не допер как его убрать нее меняя первой

    #может быть несколько ссылков родном абзаце, циклом проходимся по каждой
    for one_link in result:
        if one_link[0] in ready_links: #проверка на повторяющиеся ссылки
            continue
        text = text.replace(one_link[0], f'<a href="{one_link[0]}" target="_blank">{one_link[0]}</a>')
        ready_links.append(one_link[0])


    return text