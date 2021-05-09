var input_border_help_wrapper = ` <div class="input_border_help_wrapper"></div>`;

//Вставляем теги подписки/блока
function tag_cell(tag_name, sub) {

    return `<div class="section_config_tag">
<div class="section_config_tag_name">${tag_name}</div>
<div class="section_config_tag_btn ${sub}"></div>
</div>`;
}

function input_border_help(tag) {
    return `<div class="input_border_help">
${tag}
</div>`
}


//
//
//Подписываем и обрабатываем "-"
//
//
document.addEventListener('DOMContentLoaded', event_tags_remove());
function event_tags_remove() {
    document.querySelectorAll('.section_config_tag_btn').forEach(block => {
        block.removeEventListener('click', sub_del_tag, false);
    });
    document.querySelectorAll('.section_config_tag_btn').forEach(block => {//подписываем все "-" на событие удаления тега
        block.addEventListener('click', sub_del_tag)
    });
}

function sub_del_tag() {
    let tag_name = this.parentNode.querySelector('.section_config_tag_name').innerHTML;
    if (this.classList.contains('block')) {
        ajax_delete_tag(false, tag_name)
    }
    if (this.classList.contains('sub')) {
        ajax_delete_tag(true, tag_name)
    }
    this.parentNode.remove();
}




//
//
//делаем подписку, блокировку на теги
//
//
document.querySelectorAll('.section_config_filters_btn').forEach(block => {//подписываем оба "+" на событие тега
    block.addEventListener('click', (event) => {
        let tag_text = event.target.parentNode.querySelector('input').value;
        if (tag_text.length < 3) {
            system_alert('теги начинаются от 3-х букв')
            return
        }
        if (tag_text.length > 20) {
            system_alert('теги длинной до 20-ти букв')
            return
        }
        let tags_wrapper = event.target.parentNode.parentNode.parentNode.querySelector('.tags_wrapper');
        if (chek_already_tag(tag_text)) {
            system_alert('такой тег уже отмечен');
            return
        }
        if (event.target.classList.contains('tag_sub')) {//если кнопка "+" с классом  tag_sub значит подписка
            tags_wrapper.insertAdjacentHTML("beforeEnd", tag_cell(tag_text, 'sub'));
            ajax_tags_sub_block(true, tag_text)
            event.target.parentNode.querySelector('input').value = '';
            event_tags_remove();
            return
        }
        if (event.target.classList.contains('tag_block')) {//если кнопка "+" с классом  tag_block значит блокировка
            tags_wrapper.insertAdjacentHTML("beforeEnd", tag_cell(tag_text, 'block'));
            ajax_tags_sub_block(false, tag_text)
            event.target.parentNode.querySelector('input').value = '';
            event_tags_remove();

            return
        }

        system_alert('Ошибка связи с сервером, изменения не сохранены.');
        return

    })
});

function chek_already_tag(serch_tag) {//проверка на повторяющиеся теги при подписке/блокировке
    let status = false;
    document.querySelectorAll('.section_config_tag').forEach(block => {
        if (block.textContent.trim() == serch_tag)
            status = true;
        return
    });
    return status
}



//
//
//
//построение выпадающего списка с тегами и управлкение  им
//
//

document.querySelectorAll(".form_tags").forEach(block => {//прерываем отправку с форм подписки/отписки тегов т.к. button перехватывает событе Enter от input 
    block.addEventListener("submit", function (event) {
        event.preventDefault();
        if (event.target.querySelector('input') == document.activeElement) {//проверка на фокус нашего input
            return false;
        }
        return true;
    });
});

document.querySelectorAll(".input_tags").forEach(input => {
    input.addEventListener("keyup", function (event) {//событие при прике в нашем input теге



        //узнаем текущий тег
        let input_text = event.target.value;
        if (input_text.length < 2) {
            if (document.querySelector('.input_border_help_wrapper')) {
                document.querySelector('.input_border_help_wrapper').remove();//удаляем подсказки, если длинна тега меньше 2-ух(например пользователь нашал backspace)
            }
            return
        }

        //действия со стрелками
        if (document.querySelector('.input_border_help_wrapper') != null) {
            if (event.key == 'ArrowDown') {
                input_border_help_dawn_select(this)
                return
            }
            if (event.key == 'ArrowUp') {
                this.selectionStart = this.value.length;//переносим корретку в начало input при нажатии стрелки вверх            
                document.querySelector(".input_border").selectionStart = document.querySelector(".input_border").value.length;//переносим корретку в начало input при нажатии стрелки вверх
                input_border_help_up_select(this);
                return
            }
            if (event.key == 'Enter') {
                event.preventDefault();//прерывает событие т.к. Enter сразу ловит button
                select_tag_in_input(event.target);
                return
            }
        }



        //конструктор/деконструктор выпадающего списка
        if (document.querySelector('.input_border_help_wrapper') != null)
            document.querySelector('.input_border_help_wrapper').remove();



        if (input_text.length < 2)
            return

        var tgas_values = ajax_tags_help_serch(input_text);

        if (tgas_values.length == 0) {//если пришел пустой массив, несоздаем оболочку для списка подсказок
            return
        }



        event.target.insertAdjacentHTML("afterEnd", input_border_help_wrapper);//создаем оболочку для списка подсказок

        let tags_input_help_cell = '';

        tgas_values.forEach(value => {
            tags_input_help_cell += input_border_help(value);
        });


        document.querySelector('.input_border_help_wrapper').insertAdjacentHTML("beforeEnd", tags_input_help_cell);//вставляем варианты подсказок тегов в оболочку
        document.querySelector(".input_border_help").classList.add('help_select');//выделаем первую подсказку


        //делаем подписку на события

        document.querySelectorAll(".input_border_help").forEach(block => {
            block.addEventListener("mouseenter", tags_input_help_select);//делаем тег активным при наведении мышкой

        });

        document.querySelectorAll(".input_border_help").forEach(block => {
            block.addEventListener("click", () => select_tag_in_input(event.target));//добвляем тег в input при клике
        });
        input_border_help_count();

    });
});



function input_border_help_up_select() {//переносим выделение на один блок вверх(вызывается при нажатии стрелки вверх) 
    let select_block = document.querySelector(".input_border_help.help_select");
    let select_block_number = serch_block_index('input_border_help', select_block)
    if (select_block_number == 0) {//если блок верхний, выделяем нижний
        document.querySelector('.input_border_help.help_select').classList.remove('help_select');
        document.querySelectorAll('.input_border_help')[tags_input_help_count].classList.add('help_select');
        return
    }
    document.querySelector('.input_border_help.help_select').classList.remove('help_select');
    document.querySelectorAll('.input_border_help')[select_block_number - 1].classList.add('help_select');

}
function input_border_help_dawn_select() {//переносим выделение на один блок вниз(вызывается при нажатии стрелки вниз) 
    let select_block = document.querySelector(".input_border_help.help_select");
    let select_block_number = serch_block_index('input_border_help', select_block);
    if (select_block_number == input_border_help_count()) {//если блок нижний, выделяем верхний
        document.querySelector('.input_border_help.help_select').classList.remove('help_select');
        document.querySelectorAll('.input_border_help')[0].classList.add('help_select');
        return
    }

    document.querySelector('.input_border_help.help_select').classList.remove('help_select');
    document.querySelectorAll('.input_border_help')[select_block_number + 1].classList.add('help_select');

}

function all_tags_input_help_unselect() {
    document.querySelectorAll('.input_border_help').forEach(block => {
        block.classList.remove('help_select');
    })
}

function tags_input_help_select() {//даем тегу выделение (вызывается при наведении мышкой)
    all_tags_input_help_unselect();
    this.classList.add('help_select');
}

function select_tag_in_input(input) {//вставляем выбраный пункт из списка



    let select_tag = document.querySelector('.input_border_help.help_select').innerHTML;
    input.value = select_tag
    document.querySelector('.input_border_help_wrapper').remove();
}


//расчет и изменени/возврат количества тегов-подсказок со счетом нуля. Что бы было легче работать с массивом
var input_border_help_count
function input_border_help_count() {
    tags_input_help_count = document.querySelectorAll('.input_border_help').length - 1;
    return tags_input_help_count;
}

//ajax запрос для получения списка тегов. Посылвет чать слова, получет 10 значений с наибольшим количеством постов. Сервер преобразует ответ в JSON
function ajax_tags_help_serch(input_text) {

    var server_data = []
    request = { 'csrfmiddlewaretoken': get_cookie('csrftoken'), 'tag': input_text }

    $.ajax({
        type: 'POST',
        url: 'help_serch_tags/',
        data: request,
        async: false,
        success: function (response) {
            server_data = response;
        }
    })

    return server_data
}


//запрпос на загрузку постов, возвращает HTML
var isurl = 'get_posts/';//адрес для запроса постов
function ajax_load_content() {
    //В запросе нет списка просмотренных постов. Зачем она на странице пользователя?
    if(isurl == 'get_comments_user/'){//если комментарии
        
        return {'not_posts': get_commets()}
    }

    posts = ajax_load_posts();
    return JSON.parse(posts)

}

function ajax_load_posts () {
    var posts = null
    $.ajax({
        type: 'POST',
        url: isurl,
        async: false,
        data: { 'page': page_number, 'csrfmiddlewaretoken': get_cookie('csrftoken')},
        success: function (response) {
            posts = response;
        }
    });
    page_number += 1
    return posts
}