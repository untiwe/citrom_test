var months =["января", "февраля", "марта", "апреля", "мая", "июня", "июля", "августа", "сентября", "октября", "ноября", "декабря"];

//запрпос на загрузку постов, возвращает HTML
function ajax_load_content() {
    let page_content_wrapper = document.querySelector('.page_content_wrapper')//вставка перед block_for_scroll не подходит. page_content_wrapper не дает сообщениям выйти за пределы
    var messages = null
    $.ajax({
        type: 'POST',
        url: '',
        async: false,
        data: { 'page': page_number, 'csrfmiddlewaretoken': get_cookie('csrftoken')},
        success: function (response) {
            if (check_server_errors(response)){
                messages = 'not user'
                return
            }
            messages = response;
        }
    });
    if (messages == 'not user'){//если пользователь на чужой странице
        return
    }
    page_number += 1
    let messagesHTML = messages_generator(messages)
    page_content_wrapper.insertAdjacentHTML('beforeend', messagesHTML);
    return {'not_posts': messages}
}

function messages_generator(messages) {

    let messagesHTML = '';

    messages.forEach(one_message => {
        switch(one_message.type) {
            case 'comment_post': 
                messagesHTML += construct_comment_post (one_message)
                break;
            case 'answer_comment':
                messagesHTML += construct_answer_comment (one_message)
                break;
            case 'post_delete_moderator':
                messagesHTML += construct_post_delete_author (one_message)
                break;
            case 'post_delete_author':
                messagesHTML += construct_post_delete_moderator (one_message)
                break;
            case 'comment_delete_author':
                messagesHTML += construct_comment_delete_author (one_message)
                break;
            case 'comment_delete_moderator':
                messagesHTML += construct_comment_delete_moderator (one_message)
                break;
          
        }
    })

    return messagesHTML;


}
// comment_post
// answer_comment
function format_date(date_string){
    let date = new Date(date_string)
    return `${date.getDate()} ${months[date.getMonth()]} ${date.getFullYear()}`
}

function construct_comment_post (message){
    let m = JSON.parse(message.text);
    return `<div class="message_wrapper">
                <div class="message_date">${format_date(message.date_create)}</div>
                <h2 class="message_name">К посту: <a href="/post/${m.post_id}">${m.post_name}</a> оставили комментарий</h2>
                <p class="message_text"><a href="/user/${m.this_comment_author}">${m.this_comment_author} </a>${add_br_text(m.comment_text)}</p>
                <a class="message_link" href="/post/${m.post_id}">Ответить</a>
            </div>`
}


function construct_answer_comment (message){
    let m = JSON.parse(message.text);
    return `<div class="message_wrapper">
                <div class="message_date">${format_date(message.date_create)}</div>
                <h2 class="message_name">Вам ответили</h2>
                <p class="message_text"><a href="/user/${m.this_comment_author}">${m.this_comment_author} </a>${add_br_text(m.comment_text)}</p>
                <a class="message_link" href="/post/${m.post_id}">Ответить</a>
            </div>`
}

function construct_post_delete_author(message) {
    let m = JSON.parse(message.text);
    return `<div class="message_wrapper">
                <div class="message_date">${format_date(message.date_create)}</div>
                <h2 class="message_name">Вы удалили свой пост <a>${m.post_name}</a> </h2>
                <p class="message_text">По причине: ${m.cause}</p>
            </div>`
}

function construct_post_delete_moderator(message) {
    let m = JSON.parse(message.text);
    return `<div class="message_wrapper">
                <div class="message_date">${format_date(message.date_create)}</div>
                <h2 class="message_name">С сожалению, ваш пост: <a>${m.post_name}</a> был удален.</h2>
                <p class="message_text">Причина: ${m.cause}</p>
            </div>`
}

function construct_comment_delete_author(message) {
    let m = JSON.parse(message.text);
    return ` <div class="message_wrapper">
                <div class="message_date">${format_date(message.date_create)}</div>
                <h2 class="message_name">Вы удалили свой комментарий к посту: <a href="/post/${m.comment_post_id}">${m.comment_post_name}</a></h2>
                <p class="message_text">По причине: ${m.cause}</p>
            </div>`    
}

function construct_comment_delete_moderator(message) {
    let m = JSON.parse(message.text);
    return ` <div class="message_wrapper">
                <div class="message_date">${format_date(message.date_create)}</div>
                <h2 class="message_name">Ваш комментарий к посту: <a href="/post/${m.comment_post_id}">${m.comment_post_name}</a> был удален модератором</h2>
                <p class="message_text">По причине: ${m.cause}</p>
            </div>`    
}

