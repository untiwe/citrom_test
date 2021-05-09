function serch_block_index(selector, this_block) {//функция поиска индекса текущего блока среди остальных в родителе. Поиск идет по классу(selector)
    //this_block - сам искомый объект. Если блок не найден, возвращает -1
    //используется для поиска индекса активного блока в выпадающих меню подсказок и в конструкторе постов
    var children = document.getElementsByClassName(selector);
    var num = 0;
    for (var i = 0; i < children.length; i++) {
        if (children[i] == this_block) return num;
        if (children[i].nodeType == 1) num++;
    }
    return -1;
}

//функия для чтения куки по названию.
//чество взята отсюда https://learn.javascript.ru/cookie#getcookie-name
function get_cookie ( cookie_name ){
    var results = document.cookie.match ( '(^|;) ?' + cookie_name + '=([^;]*)(;|$)' );
    
    if ( results )
        return ( unescape ( results[2] ) );
    else
        return null;
}


function set_long_cooke(name, value='true'){
    document.cookie = `${name}=${value};  path=/; expires=Tue, 1 Jan 2100 00:00:00 GMT`;
}

function del_cookie(name) {
    document.cookie = `${name}=default_value; path=/;  expires=Tue, 1 Jan 2000 00:00:00 GMT`;

}

//
//
//для генерации комментариве(частично) вынесено в библиотеку т.к. они есть на странице поста и пользователя
//
//
//Вставлем текст комментария
function construct_comment_text(text) {
    if (text == undefined){
        return ''
    }
    
    text = convert_links(text) //оборачиваем ссылки
    text = add_br_text(text)//добавляем переносы текста
    return `<p class="comment_cell comment_content">${text}</p>`

}
//Вставляем фото комментария
function construct_comment_photo(photo) {
    if (photo == undefined){
        return ''
    }
    return `<p class="comment_cell"><img src="${photo}"></p>`

}
//Выбираем оценку вниз(нажата или нет)
function construct_comment_dawn_arrow(eval){
    if (eval == -1){
       return small_dislike_eval_src
    }
    else{
        return small_dawn_neutral_eval_src
    }
}
//Выбираем оценку вверх(нажата или нет)
function construct_comment_up_arrow(eval){
    if (eval == 1){
       return small_like_eval_src
    }
    else{
        return small_up_neutral_eval_src
    }
}
//Вставляем кнопку удаления, если нужно
function construct_comment_may_change(change){
   if(change){
       return`<img class="comment_header_cell comment_header_del_icon" onclick="delete_comment(this)" src="../../static/img/delete_icon.svg" alt="удалить пост">`
   }
   else{
       return ``
   }
}

//получаем id поста, возвращаем ссылку на него (используется в комментариях и постах)
function href_post(post_id){
    if (post_id){
    return `/post/${post_id}`
    }
    else{
        return `#`
    }
}

//получаем username пользователя, возвращаем ссылку на него (используется в комментариях и постах)
function href_user(username){
    if (username){
        return `/user/${username}`
        }
        else{
            return `#`
        }
}


//Проверка на ошибоки от сервера, если есть ошибки, вернет true
function check_server_errors(response) {

    if (response.indexOf('error') == 0) {//
        var text_error = response.substr(6);
        text_error = text_error.replace(/\['/g, '')
        text_error = text_error.replace(/\']/g, '')
        system_alert(text_error);
        return  true
    }
    else{
        return false
    }
}


//
//
//Выводим сообщения об отсутвии контента
//
//
var content_wrapper = document.querySelector('.page_content_wrapper')
function  end_conetnt_message() {
    clear_content_message()
    message_HTML = `<div class="no_contennt">Апплодисменты! Ты долистал до конца👏</div>`
    content_wrapper.insertAdjacentHTML('beforeend', message_HTML);
}
function  no_conetnt_message() {
    clear_content_message()
    message_HTML = `<div class="no_contennt">Увы, тут пока ничего нет☹️</div>`
    content_wrapper.insertAdjacentHTML('beforeend', message_HTML);
}

//Если по каким то причинам контенет догружается после вывода сообщения(в кабинете пользователя он удаляется и догружается снова БЕЗ ОБНОВЛЕНИЯ странциы), то сообщение будет не внизу.
//по этому мы убираем сообщение о контекте
function  clear_content_message() {
    document.querySelectorAll('.no_contennt').forEach(block => {//По идее, больше одного сообщения быть не должно, но на всякий случай сдела выбор и удавление всех сообщений
        block.remove()
    })
    
}

//функция получает текст. Если там есть ссылка, оборачивает ее в тег <a>
function convert_links(text) {
    let re = /([^\"=]{2}|^)((http?|https?|ftp):\/\/\S+[^\s.,> )\];'\"!?])/g; 
    let subst = '$1<a href="$2" target="_blank">$2</a>'; 
    let withlink = text.replace(re, subst);
    return withlink
}

//экранируем HTML
//источник https://coderoad.ru/24816/%D0%AD%D0%BA%D1%80%D0%B0%D0%BD%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5-%D1%81%D1%82%D1%80%D0%BE%D0%BA-HTML-%D1%81-%D0%BF%D0%BE%D0%BC%D0%BE%D1%89%D1%8C%D1%8E-jQuery
var entityMap = {
    '<': '&lt;',
    '>': '&gt;',
    //другие не надо
    //   '"': '&quot;',
    //   "'": '&#39;',
    //   '/': '&#x2F;',
    //   '`': '&#x60;',
    //   '=': '&#x3D;'
    //   '&': '&amp;',
};
function escape_text(text) {
    return String(text).replace(/[<|>]/g, function (s) {
        return entityMap[s];
      });
}

//заменяет /n на <br> полезно применять после экранирования 
function add_br_text(html_text) {
    text_out = html_text.replace(/\n/g, function (s) {
        return '<br>';
    });
    return text_out
}
