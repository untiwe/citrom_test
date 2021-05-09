//тот файл загружается, только если пользователь зашел на свою страницу


document.querySelectorAll('.tabs_btn').forEach(block => {
    block.addEventListener('click', swap_tabs);
});

//
//
//Конструктор табов: 'Посты' 'Коментарии' 'Понравилось' 'Не понравилось'
//
//

function swap_tabs(event) {
    /*Выбираем вкладку --> удаляем все посты --> отписываемся --> удаляем посты  --> подписываемся на загрузку. 
    Отписка/подписка была сделана для того, что бы не "ломалось" событие.
    Если нажали на вкладку с и постов/комментариев нету/мало и блок для скролла виден постоянно то при переключении на др. вкладку, событие не будет работать*/

    ;
    if (event.target.classList.contains('tabs_btn_active'))//если нажали по уже выбраному элементу
        return

    block_for_scroll = document.querySelector('.block_for_scroll')
    observer_page.unobserve(block_for_scroll);//отписываемя от подгрузки постов/комметанриев

    let select_tab = event.target.dataset.tab;

    document.querySelector('.tabs_btn_active').classList.remove('tabs_btn_active');
    event.target.classList.add('tabs_btn_active');
    
    let selector_target_remove = '.post'
    if(document.querySelector('.comment') != null)//если сейчас загружены комментарии, а не посты
        selector_target_remove = '.comment'
    document.querySelectorAll(selector_target_remove).forEach(block =>{
        block.remove();
    })
    
    page_number = 1//делаем нумерацию опять с первой страницы
    //определяем url для запроса постов
    
    if (select_tab == 'posts')
        isurl = 'get_posts/';
    if (select_tab == 'comments')
        isurl = 'get_comments_user/'
    if (select_tab == 'likes')
        isurl = 'like_posts/';
    if (select_tab == 'dislikes')
        isurl = 'dislike_posts/'

    observer_page.observe(block_for_scroll)//подписываемся на подгрузку постов/комметанриев
    //////////////////////////////////////////////////////////////////////////////////////////
    //Загрузка готовых постов в сервера. Начало

    // let content = ajax_content_requst(select_tab);//подаем запрос на сервер

    // document.querySelector('.tabs_content').innerHTML = ''
    // document.querySelector('.tabs_content').insertAdjacentHTML("beforeEnd", content);//вставляеп ответ сервера
    //Загрузка готовых постов в сервера. Rонец
    //////////////////////////////////////////////////////////////////////////////////////////

}

//////////////////////////////////////////////////////////////////////////////////////////
//Загрузка готовых постов в сервера. Начало

// function ajax_content_requst(type_content) {
//     if (type_content == 'posts')
//         return output_posts();
//     if (type_content == 'comments')
//         return output_comments();

//     if (type_content == 'likes')
//         return output_like_posts();

//     if (type_content == 'dislikes')
//         return output_dislike_posts();
//     return 'не понял???'

// }


// function output_comments() {
//     var content = 'привет'
//     $.ajax({
//         type: 'GET',
//         url: 'getcomments/',
//         async: false,
//         success: function (response) {
//             content = response
//         }
//     })
//     return content
// }

// function output_like_posts() {
//     var content = 'привет'
//     $.ajax({
//         type: 'GET',
//         url: 'like_posts/',
//         async: false,
//         success: function (response) {
//             content = response
//         }
//     })
//     return content
// }

// function output_dislike_posts() {
//     var content = 'привет'
//     $.ajax({
//         type: 'GET',
//         url: 'dislike_posts/',
//         async: false,
//         success: function (response) {
//             content = response
//         }
//     })
//     return content
// }

//Загрузка готовых постов в сервера. Rонец
//////////////////////////////////////////////////////////////////////////////////////////


//ajax для смены пароля
//change_password_form это id формы для смены пароля
change_password_form.addEventListener('submit', (event) => {
    event.preventDefault()
    form = new FormData(change_password_form);
    form.append('csrfmiddlewaretoken', get_cookie('csrftoken'));

    $.ajax({

        type: 'POST',
        url: '/usermanager/change_password/',
        // cache: false,
        processData: false,
        contentType: false,
        data: form,
        success: function (response) {

            if (response.indexOf('error') == 0) {
                var text_error = response.substr(6);
                text_error = text_error.replace(/\['/g, '')
                text_error = text_error.replace(/\']/g, '')
                system_alert(text_error)
            }
            if (response == 'ok') {
                change_password_form.getElementsByTagName('input')[0].value = "";
                change_password_form.getElementsByTagName('input')[1].value = "";
                change_password_form.getElementsByTagName('input')[2].value = "";
                system_alert('Пароль успешно изменен', 'green')
            }


        }
    });
})


//ajax для изменения информации о пользователе
//info_user_form это id формы с информацией о пользователе
info_user_form.addEventListener('submit', (event) => {
    event.preventDefault()
    form = new FormData(info_user_form);
    form.append('csrfmiddlewaretoken', get_cookie('csrftoken'));

    $.ajax({

        type: 'POST',
        url: '/usermanager/info_user/',
        // cache: false,
        processData: false,
        contentType: false,
        data: form,
        success: function (response) {
            if (response.indexOf('error') == 0) {
                var text_error = response.substr(6);
                system_alert(text_error)
            }
            if (response == 'ok') {
                system_alert('Изменения сохранены', 'green')
            }
        }
    });
})




function ajax_tags_sub_block(command, tag) {//тут ajax запрос на подписку/блокировку тега в зависимости от значения "command" true-полдписать false-заблокировать
    request = { 'csrfmiddlewaretoken': get_cookie('csrftoken'), 'tag': tag, 'command': command }

    $.ajax({
        type: 'POST',
        url: '/usermanager/add_tags/',
        data: request,
        success: function (response) {
            if (response != 'ok') {
                system_alert('Ошибка сервера придобавлении тега')
            }
        }
    })

}


function ajax_delete_tag(command, tag) {//запрост для удаления тегов из полей "Отслеживать теги" и "Скрывать теги"
    request = { 'csrfmiddlewaretoken': get_cookie('csrftoken'), 'tag': tag, 'command': command }
    $.ajax({
        type: 'POST',
        url: '/usermanager/delete_tags/',
        data: request,
        success: function (response) {
            if (response != 'ok') {
                system_alert('Ошибка сервера, блокировки тега')
            }
        }
    })

}

//
//
//Загружаем и вставлячем комментарии
//
//

function get_commets() {
    let comments = ajax_get_commets()
    // if(comments.comments_list.length == 0){//если нет комментариев
    //     return {}
    // }
    comments_generator(comments);
    return comments.comments_list //возвращаем объект комментариев пользователя, для адекватного расчета и вывода сообщения, конца/отсутствия контекта

}

function ajax_get_commets() {
    var comments_list = null
    $.ajax({
        type: 'POST',
        url: isurl,
        async: false,
        data: { 'page': page_number, 'csrfmiddlewaretoken': get_cookie('csrftoken')},
        success: function (response) {
            comments_list = response;
        }
    });
    page_number += 1
    return comments_list    
}

function comments_generator(object_comments) {
    let scope = document.querySelector('.page_content_wrapper');
    object_comments.comments_list.forEach(comment => {
        let html_comment = `<div class="comment" data-id="${comment.id}">
                                <div class="comment_header">
                                    <a href="${href_user(comment.username)}" class="comment_header_cell comment_header_avatar"><img
                                            src="${comment.avatar}"></a>
                                    <a href="${href_user(comment.username)}" class="comment_header_cell comment_header_author">${comment.username}</a>
                                    <img class="comment_header_cell comment_header_dawn_small_arrow"
                                        onclick="eval_comment(this.parentNode, false)"
                                        src="${construct_comment_dawn_arrow(comment.eval)}">
                                    <div class="comment_header_cell comment_header_count">${comment.rating}</div>
                                    <img class="comment_header_cell comment_header_up_small_arrow"
                                        onclick="eval_comment(this.parentNode, true)" 
                                        src="${construct_comment_up_arrow(comment.eval)}">
                                        ${construct_comment_may_change(comment.may_change)}
                                </div>
                                ${construct_comment_text(comment.comment_text)}
                                ${construct_comment_photo(comment.comment_photo)}
                                <a href="${href_post(comment.post_id)}" class="comment_cell comment_footer">Перейти</a>
                            </div>`
        scope.insertAdjacentHTML("beforeend", html_comment);
    })
}

//
//
//Загрузка аватара пользователя
//
//
load_avatar.addEventListener('change', refresh_avatar);//подписываемся на событие выбора файлов для загрузки
var user_avatar = document.querySelector('.user_info_avatar img')
function refresh_avatar(evt) {
    let file = evt.target.files[0]; // files всегда массив, но у нас тут только 1 файл
    

    // Only process image files.
    if (!file.type.match('image.*')) {
        alert("Только изображения...");
        return
    }
    //5242880
    if (file.size > 6291456) {//6291456 Байт это 6 Мегабайт. Оставил с запасом
        alert("Размер картинки не больше 5-ти Мегабайт");
        return
    }

    //ставим анимацию загрузки
    user_avatar.classList.add('avatr_spiner')
    user_avatar.src = '../../static/img/loading_arrows_blue.svg'

    let reader = new FileReader();

    // Closure to capture the file information.
    reader.onload = (function (theFile) {
        return function (e) {
            ajax_load_coment_photo(theFile);
        };
    })(file);

    //Read in the image file as a data URL.
    reader.readAsDataURL(file);
   

}

function ajax_load_coment_photo(f) {//функия ajax для вставки фотографий после их загрузки
    var formData = new FormData();
    formData.append('photo', f);
    formData.append('csrfmiddlewaretoken', get_cookie('csrftoken'));
    
    $.ajax({
        url: '/usermanager/new_avatar/',
        type: 'POST',
        data: formData,
        cache: false,
        processData: false,
        contentType: false,
        success: function (response) {
            if (check_server_errors(response)){
                return  
            }
            //убираем анимацию, вставляем новый аватар
            user_avatar.classList.remove('avatr_spiner')
            user_avatar.src = response
            //обновляем аватар в sitebar
            document.querySelector('.user_avatar img').src = response
        }
    });

}

//
//
//Удаление аватара пользователя(установка стандартного)
//
//
document.querySelector('.right_btn').addEventListener('click', delete_avatar);//подписываемся на событие выбора файлов для загрузки

function delete_avatar(){
    $.ajax({
        url: '/usermanager/del_avatar/',
        type: 'POST',
        data: { 'csrfmiddlewaretoken': get_cookie('csrftoken')},
        success: function (response) {
            if (check_server_errors(response)){
                return  
            }
            user_avatar.src = response
            system_alert('аватарка удалена', 'green')
            //обновляем аватар в sitebar
            document.querySelector('.user_avatar img').src = response
        }
    });
}