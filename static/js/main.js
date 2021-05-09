

var return_password_form = `<form action="#" method="POST" class="temp_class_1 user_window_wrapper">
<p class="user_sell email_message">Введите ваш почтовый адрес для восстановления</p>
<input class="user_sell input_user input_email_password"  type="email" name="name" placeholder="Почта" required>
<p class="temp_class_1 user_sell return_password_button" type="submit">Восстановаить</p>
<span class="or">или</span>
<p class="temp_class_1 user_sell register_button">Регистрация</p>
</form>`;



var back = document.querySelector('body');
//активатор кнопки бургера
let header__burger = document.querySelector('.menu-btn');
let header_menu = document.querySelector('.nav_header');
header__burger.onclick = function () {
    header__burger.classList.toggle('active');
    header_menu.classList.toggle('active');
    back.classList.toggle('lock');
}
//активатор кнопки сайтбара
let sitebar_btn = document.querySelector('.sitebar_btn');
let sitebar = document.querySelector('.sitebar');
sitebar_btn.onclick = function () {
    sitebar_btn.classList.toggle('active');
    sitebar.classList.toggle('active');
    back.classList.toggle('lock');
}


//вешаем собыите за кнопку "Регистрация" если она есть
document.addEventListener('DOMContentLoaded', register_button_click)
function register_button_click() {
    let register_btn = document.querySelector('.register_button');
    if (register_btn) {
        register_btn.addEventListener('click', registration_form);
    }
}


function registration_form() { //загрузка формы регистрации вместо формы входа по кнопке "Регистрация"

    document.querySelector('.user_window_wrapper').remove();

    // это было вставленно на этапе верстки reg_form - перменная с html колом
    //document.querySelector('.sitebar').insertAdjacentHTML('afterBegin', reg_form)
    // теперь вместо него функция reg_form Она отправляет ajax запрос и вставляет полученую форму
    reg_form();
    document.querySelector('.user_window_wrapper').onsubmit = (event) => { //событие на новую кнопку регистрации
        //делаем валидацию формы
        let wrapper = event.target;
        let message = document.querySelector('.reg_message');
        if (wrapper[0].value.length < 4) {//проверка длинны логина
            message.textContent = 'Длинна логина не менее 4-ех символов';
            return false
        }
        if (wrapper[1].value.length < 6) {//проверка длинны пароля
            message.textContent = 'Длинна пароля не менее 6-ти символов';
            return false

        }
        if (wrapper[1].value !== wrapper[2].value) {//проверка совпадения пролей
            message.textContent = 'Пароли не совпадают';
            return false
        }
        ajax_sed_new_user();
        return false
    }
}



//вешаем собыите за кнопку "забыл пароль" если она есть
var no_password_btn = document.querySelector('.no_password');
if (no_password_btn) {
    no_password_btn.addEventListener('click', form_return_password);
}



function form_return_password() {//загружаем форму восстановления пароля
    document.querySelector('.user_window_wrapper').remove();
    document.querySelector('.sitebar').insertAdjacentHTML('afterBegin', return_password_form)
    document.querySelector('.return_password_button').addEventListener('click', sand_password_email);
    register_button_click()
    

}
//отправляем email на сервер для смены пароля
function sand_password_email() {
    let email_massage = document.querySelector('.email_message');
    let email = document.querySelector('.input_email_password').value;

    var reg = /^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$/;
    if(reg.test(email) == false) {
        email_massage.textContent = 'Введен не правильный email адресс'
        return false;
    }

    $.ajax({
        type: 'POST',
        url: '/usermanager/reset_password/',
        data: { 'email': email, 'csrfmiddlewaretoken': get_cookie('csrftoken') },
        success: function (response) {
            if (response.indexOf('error') == 0) {
                email_massage.innerHTML = `Что то пошло не так. Проверьте правильноcть почтнового ящика или напишитье <a href="./aboutus#feedback_form">нам</a>`;
                return
            }
            email_massage.innerHTML = 'Всё ок, пиьсмо с паролем отправленно. Если будут вопросы, напишитье <a href="./aboutus#feedback_form">нам</a>'
        }
    });

}


//
//
// Изменнеие главных тегов(switch) в сайтбаре
//
//
document.querySelectorAll('.config_switch input').forEach(block => {//подпска на изменение switch
    
    block.addEventListener('change', (event) => {
        
        document.querySelector('.message_reload').style.display = 'block';//вывод сообщения о перезагрузке, что бы не отрывать пользователя от места просмотра + как мы еще прочитаем куки?
        set_settings_views()//Проходимся по настройкайм и фиксируем соответсвующие изменения
        
    });
});

//записываем или удаемя куки при изменени опций просмотра
function set_settings_views() {
    if(old_18){//перменная ставится сервером если тут false, сервер вообще не отрисовал этот параметр switch
        if (nsfw.checked){
            set_long_cooke('nsfw')
        }
        else{
            del_cookie('nsfw')
        }
    }

    if (gore.checked){
        set_long_cooke('gore')
    }
    else{
        
        del_cookie('gore')
    }
    if (politic.checked){
        set_long_cooke('politic')
    }
    else{
        del_cookie('politic')
    }

    if (hide_view.checked){
        set_long_cooke('hide_view')
    }
    else{
        del_cookie('hide_view')
    }

    
    
    
}





//
//
//
// Оценки постов
//
//
function eval_post(post_footer, command) { //при клике на оценку поста: меняем стрелку, меняем счетчик методом post_count
    if(post_preview){//если у нас предпросмотр поста
        return
    }
    let post_id = post_footer.dataset.post
    eval_post_ajax(post_id, command)//Посылаем запрос изменния рейтинга. Цвет меняем независимо



    var dislike_eval = post_footer.getElementsByTagName('img')[1];
    var like_eval = post_footer.getElementsByTagName('img')[2];
    var increment = 0

    //меняем цает стрелок и определаем на сколько поменять рейтинг поста
    if (command == true) {
        if (dislike_eval.src.indexOf('big_dislike_eval') != -1) {
            dislike_eval.src = big_dawn_neutral_eval_src
            increment++
        }
        if (like_eval.src.indexOf('big_up_neutral_eval') != -1) {
            increment++
            like_eval.src = big_like_eval_src
        }
        else {
            increment--
            like_eval.src = big_up_neutral_eval_src;
        }
    }
    if (command == false) {
        if (like_eval.src.indexOf('big_like_eval') != -1) {
            like_eval.src = big_up_neutral_eval_src
            increment--
        }
        if (dislike_eval.src.indexOf('big_dawn_neutral_eval') != -1) {
            increment--
            dislike_eval.src = big_dislike_eval_src
        }
        else {
            increment++
            dislike_eval.src = big_dawn_neutral_eval_src;
        }
    }
    post_count(post_footer, increment)

}

function post_count(post_footer, increment) {//Меняем цифру рейтинга поста
    count = Number(post_footer.querySelector('.post_count_score').textContent);
    count += increment
    post_footer.querySelector('.post_count_score').textContent = count;
}


function eval_post_ajax(post_id, command) {
    $.ajax({
        type: 'POST',
        url: '/smalltasks/eval_post/',
        async: false,
        data: { 'post_id': post_id, 'command': command, 'csrfmiddlewaretoken': get_cookie('csrftoken') },
        success: function (response) {
            check_server_errors(response);            
        }
    });
}

//
//
//Удаление поста
//
//

function delete_post(post) {
    let post_id = post.parentNode.parentNode.querySelector('.post_footer').dataset.post
    
    let cause = prompt('Вы можете указать причину', 'Не указана')
    if (cause == null || cause == ''){
        system_alert('Рады, что вы передумали!', 'green')
        return
    }

    $.ajax({
        type: 'POST',
        url: '/postmanager/delete/',
        data: null,
        data: { 'post_id': post_id, 'cause': cause, 'csrfmiddlewaretoken': get_cookie('csrftoken') },
        success: function (response) {
            if (check_server_errors(response)){
                return
            }
            else{
                system_alert('Вы удалили пост', 'green')
            }
        }
    });

}




//
//
// Функция всплывающего сообщения
//
//

document.querySelector('.system_alert_x').addEventListener('click', hidden_system_alert);//подписка 'X' для закрытия

// system_alert('Сообщение об ошибке');//тест работы
function system_alert(text, color = null) {//вывод сообщения
    document.querySelector('.system_alert').classList.add('active');
    document.querySelector('.system_alert').style.backgroundColor = 'red';
    block_massage = document.querySelector('.system_alert_text');
    block_massage.textContent = text;
    block_massage.style.display = "block";

    if (color) {
        document.querySelector('.system_alert').style.backgroundColor = color;
    }

    setTimeout(hidden_system_alert, 4000);//закрытие через 4 секнды

}

function hidden_system_alert() {
    document.querySelector('.system_alert').classList.remove('active');
    //возможно нужны задержка
    document.querySelector('.system_alert').style.backgroundColor = 'red';
}



//
//
//
// Обарабатываем кнопку "вверх"
//
//

let goTopBtn = document.querySelector('.back_to_top');

window.addEventListener('scroll', trackScroll);//вешаем событие на прокрутку
goTopBtn.addEventListener('click', backToTop);//"клик" на кнопку вверх

function trackScroll() {//показываем/непоказываем кнопку в зависимости от положения экрана на странице
    let scrolled = window.pageYOffset;
    let coords = document.documentElement.clientHeight;

    if (scrolled > coords) {
        goTopBtn.classList.add('back_to_top-show');
    }
    if (scrolled < coords) {
        goTopBtn.classList.remove('back_to_top-show');
    }
}
function backToTop() {//перемотка вверх
    if (window.pageYOffset > 0) {
        window.scrollBy(0, -80);//на 60 пикселей
        setTimeout(backToTop, 0);//с задержкой 0 секунд
    }
}


//Код на этапе верстки писался до сюда, дальше идет паралельно написаное с backend, но это не точно;)
//Код на этапе верстки писался до сюда, дальше идет паралельно написаное с backend, но это не точно;)
//Код на этапе верстки писался до сюда, дальше идет паралельно написаное с backend, но это не точно;)
//Код на этапе верстки писался до сюда, дальше идет паралельно написаное с backend, но это не точно;)
//Код на этапе верстки писался до сюда, дальше идет паралельно написаное с backend, но это не точно;)


//ajax за прос для получения формы регитсрации 
function reg_form() {

    $.ajax({
        type: 'GET',
        url: '/usermanager/reg/',
        async: false,
        data: null,
        success: function (response) {
            document.querySelector('.sitebar').insertAdjacentHTML('afterBegin', response);
        }
    });

}


//ajax запрос на регистрацию новго пользователя
function ajax_sed_new_user() {
    document.querySelector('.reg_message').textContent = '' //отчищаем сообщение
    form = new FormData(document.querySelector('.user_window_wrapper'));//создаем объект формы и пихаем в него нашу форму регистрации

    $.ajax({
        type: 'POST',
        url: '/usermanager/reg/',
        data: form,
        contentType: false,
        processData: false,
        success: function (response) {
            if (error_or_insert(response)) {
                // если окно обновислоь вешаем событие на кнопку выхода
                ajax_sed_logout();
            }
        }
    });


}

//если есть окно пользователя(смотрим наличие кнопки "выход") то вешаем событине разлогинивания
if (document.querySelector('.logout')) {
    ajax_sed_logout()
}

//ajax запрос и подписка на разлогирование
function ajax_sed_logout() {
    document.querySelector('.logout').addEventListener('click', () => {

        $.ajax({
            type: 'GET',
            url: '/usermanager/logout/',
            data: null,
            success: function (response) {
                if (error_or_insert(response)) {
                    ajax_sed_login();
                }
            }
        });

    });
}

if (document.querySelector(".user_window_wrapper input[placeholder=Логин]")) {
    ajax_sed_login()
}

//ajax запрос на авторизацию
function ajax_sed_login() {
    document.querySelector('.user_window_wrapper').addEventListener('submit', (event) => {
    event.preventDefault();
    document.querySelector('.reg_message').textContent = '' //отчищаем сообщение
    form = new FormData(document.querySelector('.user_window_wrapper'));//создаем объект формы и пихаем в него нашу форму регистрации

        $.ajax({
            type: 'POST',
            url: '/usermanager/login/',
            data: form,
            contentType: false,
            processData: false,
            success: function (response) {
                if (error_or_insert(response)) {
                    ajax_sed_logout();
                }
            }
        });

    });
}


//Функция для проверки и вывода ошибок. Если их нет, значит пришло новое окно пользователя. Его и вставояем
function error_or_insert(response) {
    if (response.indexOf('error') == 0) {
        var text_error = response.substr(6);
        text_error = text_error.replace(/\['/g, '')
        text_error = text_error.replace(/\']/g, '')
        document.querySelector('.reg_message').textContent = text_error;
        return false
    }
    else {
        //если ошибок нет, значит пришло новое окно пользователя. Его и вставляем
        document.querySelector('.user_window_wrapper').remove();
        document.querySelector('.sitebar').insertAdjacentHTML('afterBegin', response)
        return true
    }
}



//
//
// Счетчик просмотрв постов
//
//


//window.onload = views_counter(); // ждем полной загрузки страницы

function views_counter() {
    const options = {       // устанавливаем настройки
        root: null,         // родитель целевого элемента - область просмотра=
        rootMargin: '0px',  // без отступов=
        threshold: 0.5      // процент пересечения - половина изображения

    }

    // создаем наблюдатель
    const observer = new IntersectionObserver((entries, observer) => {
        // для каждой записи-целевого элемента
        
        entries.forEach(entry => {
            // если элемент является наблюдаемым
            if (entry.isIntersecting) {
                let post_footer = entry.target.parentNode
                let target_event = entry.target
                
                ajax_views_counder(post_footer)
                // прекращаем наблюдение
                observer.unobserve(target_event)
            }
        })
    }, options)

    // с помощью цикла следим за всеми '.post_eve' на странице
    document.querySelectorAll('.post_eve').forEach(i => {
        observer.observe(i)
    })
}

var post_views = []//массив уже просмотреннах постов(сбрасывается с обновлением страницы)
// не надо var local_storage_post_views = new Map()//коллекция просмотреных постов, хранит просмотренные посты
//посылаем запрос с постом у которого +1 просмотр
function ajax_views_counder(post_footer) {
    
    let post_id = post_footer.getAttribute('data-post')
    if (post_views.indexOf(post_id) != -1) {//проверяем, что пост еще не смотрели
        return
    }
    if (check_fresh_view_post (post_id)){
        return
    }
    post_views.push(post_id)//Записываем id поста хранилище до обновления страницы(по идее это лишние т.к. после прсомтра поста, с него снимается отслеживание)
    views_posts_local_strage(post_id);//Записываем id поста в локальное хранилище
    $.ajax({
        type: 'POST',
        url: '/smalltasks/post_views_counter/',
        data: { 'post_id': post_id, 'csrfmiddlewaretoken': get_cookie('csrftoken') },
    });

}

//смотрим id поста и проверяем как давно его смотрели в последний раз. Если просмотра небыло, добавляем его в local_storage
//так же удаляем те посты, просмотр которых был давно, для возможности записи нового просмотра
//весь список храним под одним ключем, дабы не "раздувать" ключи в localStorage
//если пост просмотрен, вернет true
var short_border_time = 3600000//18 часов в ms
function check_fresh_view_post (post_id){
    let now = new Date()//ставим текущее время

    

    if (localStorage.getItem('short_time_views_posts') == null){
        //первый пост записываем тут,что бы JSON.parse не парсила пустую строку и не кидала ошибок
        first_post = new Map()
        first_post[`id_${post_id}`] = new Date()
        first_post = JSON.stringify(first_post)
        localStorage.setItem('short_time_views_posts', first_post)
        //пост считается еще не просмотреным
        return false
    }
    let time_views_posts = localStorage.getItem('short_time_views_posts')
    time_views_posts = JSON.parse(time_views_posts)

    
    //если нет просмотра поста или просмотр был давно, создаем или обновляем ее в в localStorage
    if (time_views_posts[`id_${post_id}`] == undefined || now - new Date(time_views_posts[`id_${post_id}`]) > short_border_time){
        time_views_posts[`id_${post_id}`] = new Date()
        time_views_posts = JSON.stringify(time_views_posts)
        localStorage.setItem('short_time_views_posts', time_views_posts)
        //пост считается еще не просмотреным
        return false
    }
    
    //остается вариант, где просмотрен
    return true
    
}

//отчищаем localStorage.short_time_views_posts после загрузки страницы
document.addEventListener('DOMContentLoaded', () => {
    let time_views_posts = localStorage.getItem('short_time_views_posts')
    if (localStorage.getItem('short_time_views_posts') == null){
        return
    }
    let now = new Date()//ставим текущее время
    time_views_posts = JSON.parse(time_views_posts)
    
    for (i in time_views_posts){
        if (now - new Date(time_views_posts[i]) > short_border_time){
            
            delete time_views_posts[i]
        }
    }
    time_views_posts = JSON.stringify(time_views_posts)
    localStorage.setItem('short_time_views_posts', time_views_posts)
    

});

//итерация с [...] https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Spread_syntax
//Записываем id поста в локальное хранилище
function views_posts_local_strage(post_id) {
    //проверка на наличие записей, и запись первого значения
    if (localStorage.getItem('views_posts') == null) {
        localStorage.setItem('views_posts', post_id);
        return
    }
    //проверка на повторения
    let old_posts_list = localStorage.getItem('views_posts').split(',');
    if (old_posts_list.indexOf(String(post_id)) != -1) {
        return
    }
    //записываем новое значение
    let posts_list = localStorage.getItem('views_posts');
    let new_posts_list = posts_list + ',' + post_id;
    localStorage.setItem('views_posts', new_posts_list);

}

//test window.onload = () => {console.log('полная загрузка страницы');};
//test document.addEventListener('DOMContentLoaded', () => {console.log('загрузка DOM страницы');});


//
//
//
// Оценки комментариев
//
//

function eval_comment(comment_header, command) { //при клике на оценку комментария: меняем стрелку, меняем счетчик методом comment_count    
    let comment_id = comment_header.parentNode.dataset.id 
    eval_comment_ajax(comment_id, command)//Посылаем запрос изменния рейтинга. Цвет меняем независимо

    var dislike_eval = comment_header.getElementsByTagName('img')[1];
    var like_eval = comment_header.getElementsByTagName('img')[2];
    var increment = 0

    //меняем цает стрелок и определаем на сколько поменять рейтинг клмментария
    if (command == true) {
        if (dislike_eval.src.indexOf('small_dislike_eval') != -1) {
            dislike_eval.src = small_dawn_neutral_eval_src
            increment++
        }
        if (like_eval.src.indexOf('small_up_neutral_eval') != -1) {
            increment++
            like_eval.src = small_like_eval_src;
        }
        else {
            increment--
            like_eval.src = small_up_neutral_eval_src;
        }
    }
    if (command == false) {
        if (like_eval.src.indexOf('small_like_eval') != -1) {
            like_eval.src = small_up_neutral_eval_src
            increment--
        }
        if (dislike_eval.src.indexOf('small_dawn_neutral_eval') != -1) {
            increment--
            dislike_eval.src = small_dislike_eval_src;
        }
        else {
            increment++
            dislike_eval.src = small_dawn_neutral_eval_src;
        }
    }
    comment_count(comment_header, increment)

}


function comment_count(comment_header, increment) {//Меняем цифру рейтинга поста
    count = Number(comment_header.querySelector('.comment_header_count').textContent);
    count += increment
    comment_header.querySelector('.comment_header_count').textContent = count;
}


function eval_comment_ajax(comment_id, command) {
    $.ajax({
        type: 'POST',
        url: '/smalltasks/eval_comment/',
        data: { 'comment_id': comment_id, 'command': command, 'csrfmiddlewaretoken': get_cookie('csrftoken') },
        success: function (response) {
            check_server_errors(response);
        }
    });
}

function delete_comment(comment) {
    comment_id = comment.parentNode.parentNode.dataset.id
    let cause = prompt('Вы можете указать причину', 'Не указана')
    if (cause == null || cause == ''){
        system_alert('Рады, что вы передумали!', 'green')
        return
    }
    $.ajax({
        type: 'POST',
        url: '/commentmanager/delete/',
        data: {'comment_id': comment_id, 'cause' : cause, 'csrfmiddlewaretoken': get_cookie('csrftoken')},
        success: function (response) {
            if (check_server_errors(response)) {
                return
            }
            else{
                system_alert('Комментарий успешно удален', 'green')
            }
        }
    });

}

//Выводим увеличеное изображение по его клику
function expand_picture(src) {
    show_modal_window(text_header = '', HTML_conent = `<img class="post_content_img"  src=${src}>`)
    modal_window_HTML_body.classList.add('img_wrapper')
    fone_modal_window.addEventListener('click', unexpand_picture)

}

//делаем убирание картинки при клике по фону
function unexpand_picture() {
    hide_modal_window();
    fone_modal_window.removeEventListener('click', unexpand_picture)
    modal_window_HTML_body.classList.remove('img_wrapper')
}