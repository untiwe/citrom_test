window.onload = views_counter()//запускаем счетчие просмотров

function comment_img_create(src, alt) {//вынесли функцию создания блока вначало для упрощения его изменений будущем
    return `<img src="${src}" alt="${alt}">
                <div class="comment_load_photo_block"><div>Загружаем изображение</div></div>`;

}


function sub_comments(){
    document.querySelectorAll(".comment_footer").forEach(comment_perent => {//подписываем каждую кнопку "ответить" на событие клика
        comment_perent.addEventListener("click", function () {
            var clone_form = document.querySelectorAll('form.comment')[0];//записываем форму коментария в переменную .cloneNode(true);
            var id_perent = comment_perent.parentNode.id.replace(/\D+/g, '');//берем номер родительского коментария из его id, удаляя буквы
            clone_form.childNodes[3].value = id_perent;//меняем input на номер родителя, у котрого будет коментарий. Выборка идет ПО ИНДЕКСУ!!! при смене формы, он может поменяться
            document.querySelectorAll('form.comment')[0].remove();//удаляем старую форму
            comment_perent.parentNode.insertBefore(clone_form, comment_perent);
        });
    });
};

//Валидация формы комментария. Посколку она клонируется, переподписывать ее не надо
document.querySelector('form.comment').onsubmit = (event) => {//подписываем форму отправки коментария на событие отправки как сдеалать через addEventListener не нашел
    // поле текста коментария event.target.querySelector('textarea');
    // input фото коментария photo;
    event.preventDefault()
    let valid = false;
    if (!(event.target.querySelector('textarea').value.length < 5)) {
        valid = true
    }
    if (!(photo.value == '')) {
        valid = true;
    }
    if (!(valid)) {
        alert('Оставьте Фотографию или коментарий');

    }
    if (valid) {
        ajax_send_new_comment()
    }
    //можно вернуть чтоб прервать отпрвку, но уже есть preventDefault()// return false;
};




photo.addEventListener('change', new_img_block);//подписываемся на событие выбора файлов для загрузки
function new_img_block(evt) {//с помощью этой функции мы берем выбраные фотографии поста и выводим на страницу до начала загрузки(загрузка начинается паралельно)
    let files = evt.target.files; // FileList object
    let img_wrapper = document.querySelector(".comment_time_photo")
    for (let i = 0, f; f = files[i]; i++) { //функция была скопирована из констуктора поста(newpost.js), по этому цикл остался, хоть он тут и не нужен


        // Only process image files.
        if (!f.type.match('image.*')) {
            alert("Только изображения...");
            return
        }
        //5242880
        if (f.size > 6291456) {//6291456 Байт это 6 Мегабайт. Оставил с запасом
            alert("Размер картинки не больше 5-ти Мегабайт");
            return
        }

        let reader = new FileReader();

        // Closure to capture the file information.
        reader.onload = (function (theFile) {
            return function (e) {
                let photo_src = e.target.result
                let photo_alt = theFile.name
                img_wrapper.innerHTML = '';//отчищаем болок, на слуйчай, уже выбраной фотки    
                img_wrapper.insertAdjacentHTML("afterBegin", comment_img_create(photo_src, photo_alt));


                ajax_load_coment_photo(theFile, photo_src, photo_alt);
            };
        })(f);

        // Read in the image file as a data URL.
        reader.readAsDataURL(f);
    }

}

function ajax_load_coment_photo(f, src, alt) {//функия ajax для вставки фотографий после их загрузки
    //ищет каждую фото по ее уникальному alt и меняет ее src из локального она компьютере, на серверную
    var formData = new FormData();
    formData.append('photo', f);
    formData.append('csrfmiddlewaretoken', get_cookie('csrftoken'));

    $.ajax({
        url: '/post/commentphoto/',
        type: 'POST',
        data: formData,
        cache: false,
        processData: false,
        contentType: false,
        success: function (response) {
            if (check_server_errors(response)){
                document.querySelector('.comment_time_photo').innerHTML = '';//убраем временную фотографию
                return  
            }
            //получем от сервера ответ с новыми src картинки, после загрузки. А так же id картини в базе, для дальнейшей привязки к коментарию
            let new_photo = response
            document.querySelector(`img[src="${src}"]`).src = new_photo[0];
            // console.log(document.querySelector(`img[src="${new_photo[0]}"]`));
            document.querySelector(`img[src="${new_photo[0]}"]`).dataset.id = new_photo[1];
            document.querySelector(`img[src="${new_photo[0]}"]`).parentNode.querySelector('.comment_load_photo_block').remove();
        }
    });

}




//Отправлем комментарий
function ajax_send_new_comment() {

    let form = new FormData(document.querySelector('form.comment'));

    form.set('csrfmiddlewaretoken', get_cookie('csrftoken'))
    form.delete('photo');

    if (document.querySelector(`form.comment img`)) {
        let img_comment = document.querySelector(`form.comment img`).dataset.id
        form.set('photo_id', img_comment);
    }
    //добаляем id родительского комментария(если он есть)
    let perent_comment_id = document.querySelector('form.comment').parentNode.dataset.id
    if(typeof perent_comment_id != "undefined"){
        form.set('perent_comment_id', perent_comment_id);
    }
    
    $.ajax({

        type: 'POST',
        url: '/post/newcomment/',
        cache: false,
        processData: false,
        contentType: false,
        data: form,
        success: function (response) {
            if (check_server_errors(response)){
                return  
            }
            let form = document.querySelector(`form.comment`);
            form.querySelector('.comment_textarea').remove();
            form.querySelector('span').remove();
            if (form.querySelector(`img`)){
                form.querySelector(`img`).remove();
            }
            //обращаемся по id, label_comment
            label_comment.textContent = 'Сообщение отправлено'
        }
    });
}


//
//
//Загружаем и вставляем комментарии к посту
//
//
var loaded = false
var comments = null //объект со всем комментариями, обявлен глобально т.к. нужен для дочерних комментаривев в функции children
function ajax_load_content() {
    if (loaded)//делаем функцию одноразовой, отписка почему то не работает
        return null;
    loaded = true;
    comments = ajax_load_comments().comments_list;
    comments_generator(comments);

    let load_point = document.querySelector('.comments_wrapper')
    load_point.insertAdjacentHTML('afterbegin', all_commennts_HTML);
    sub_comments();//Подписываем кнопки комментариев "ответить"
    scope.insertAdjacentHTML("beforeend", yandex_rca);//вставка рекламы после комментариев
    return 'post_comments';
    
}

function ajax_load_comments(){
    var object = null
    $.ajax({
        type: 'POST',
        url: 'getcommentspost/',
        async: false,
        data: {'csrfmiddlewaretoken': get_cookie('csrftoken')},
        success: function (response) {
            object = response;
        }
    });
    return object 
}


function comments_generator(object_comments) {
    
    all_commennts_HTML = '';
    object_comments.forEach(comment => {
        if (comment.perent == 'False'){
            all_commennts_HTML += one_comment_generator(comment);
        }
    });
    return all_commennts_HTML

}

function  one_comment_generator(comment) {
    if (comment.deleted){
        return `
                <div class="comment" data-id="${comment.id}">
                    <div class="comment_header">
                        <div class="comment_header_cell comment_header_count">${comment.rating}</div>
                    </div>
                    <p class="comment_cell comment_content">коментарий удален</p>
                    ${children(comment.id)}
                </div>`
                
    }



                        
    return `<div class="comment" data-id="${comment.id}">
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
                <div class="comment_cell comment_footer">Ответить</div>
                ${children(comment.id)}
            </div>`

}

//смотрим есть ли в масиве дочерние комментари, и вызываем one_comment_generator с каждым из них
function children(perent_id) {
    let children_HTML = ''
    result = comments.filter(comment => comment.perent == perent_id);
    result.forEach(chield => {
        children_HTML += one_comment_generator(chield)
    })
    return children_HTML
}
