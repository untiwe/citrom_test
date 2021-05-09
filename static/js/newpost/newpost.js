var bool_del_local_storage = true//перменная удаления поста из storage, что бы при сбросе поста пользователем, local storage не сохранялись
//инициализируем количество блоков от 0 а не от 1
function newpost_blok_count() {
    return document.getElementsByClassName('newpost_blok').length - 1;
}


function get_buttoms (){
    return `<div class="newpost_cell_btns">
                <img class="newpost_cell_btn_blockup" src="${move_block_up_src}" alt="перместить вврех">
                <img class="newpost_cell_btn_blockremove" src="${block_remove_src}" alt="удалить">
                <img class="newpost_cell_btn_blockdawn" src="${move_block_dawn_src}" alt="перместить вниз">
            </div>`
    
}


//HTML нового блока с текстом
function html_new_text_block (text){
return `<div class="newpost_cell newpost_blok">
            <textarea class="temp_class_1 newpost_text" onkeyup="textarea_resize(this)" rows="1">${text}</textarea>
            ${get_buttoms()}
        </div>`;
}

//сохранили перед тестами
// var html_new_text_block = `<div class="newpost_cell newpost_blok">
// <div class="temp_class_1 newpost_text" contenteditable="true"></div>
// <div class="newpost_cell_btns">
//     <img class="newpost_cell_btn_blockup" src="${move_block_up_src}" alt="перместить вврех">
//     <img class="newpost_cell_btn_blockremove" src="${block_remove_src}" alt="удалить">
//     <img class="newpost_cell_btn_blockdawn" src="${move_block_dawn_src}" alt="перместить вниз">
// </div>
// </div>`;



//HTML нового блока с картинкой
function html_new_img_block(src, is_photo_loaded = false) {//вынесли функцию создания блока вначало для упрощения его изменений будущем

    let load_message = ``
    //если нет photo_id значит фото еще грузится. Если есть, зачит фото достали из local storage
    if (!(is_photo_loaded)){
        load_message = `<div class="newpost_load_photo_block"><div>Загружаем изображение</div></div>`
    }

    return `<div class="newpost_cell newpost_blok">
                <div class="temp_class_1 newpost_img"><img src="${src}">
                    ${load_message}
                </div>
                ${get_buttoms()}
            </div>`;
}

var tags_input_help_wrapper = '<div class="tags_input_help_wrapper"></div>'; //оболочка для подсказок тегов


function tags_input_help_create(tag, count) { //функия - конструктор каждого пунка подсказок тегов.
    let data = `<div class="tags_input_help">
                    <div class="tags_input_help_tag">${tag}</div>
                    <div class="tags_input_help_count">${count}</div>
                </div>`;
    return data

}

document.addEventListener('DOMContentLoaded', ready_move());//подписываем кнопки на события после загрузки документа
document.querySelectorAll(".newpost_cell_btn_blockup").forEach(block => {
    block.addEventListener("click", block_moveup)
});

function chek_blocks_count() {
    if (newpost_blok_count() >= 50) {
        return true
    }
    else
        return false
}

function block_moveup(this_block) {//функция поднятия блока вверх (по кнопке)
    this_block = this.parentNode.parentNode;// this - это кнопка, а нам нужен родитель ее родителя
    let this_block_nomber = serch_block_index('newpost_blok', this_block); //узнамем порядковый номер блока из остальных
    if (this_block_nomber == 0)//если блок первый, ничего не делаем
        return

    let clone_this_block = this_block.cloneNode(true);//клонируем блок
    this_block.parentNode.querySelectorAll(".newpost_blok")[this_block_nomber - 1].before(clone_this_block);//вставлем клон перед предыдущим блоком

    this_block.remove();//удаляем оригинальный блок
    ready_move();//запускаем подписку на события т.к. у нас есть новый блок
};
function block_movedawn(this_block) {//функция опуская блока вниз (по кнопке) почти анологична функции block_moveup
    this_block = this.parentNode.parentNode;
    let this_block_nomber = serch_block_index('newpost_blok', this_block);
    if (this_block_nomber == newpost_blok_count())
        return

    let clone_this_block = this_block.cloneNode(true);
    this_block.parentNode.querySelectorAll(".newpost_blok")[this_block_nomber + 1].after(clone_this_block);
    this_block.remove();
    ready_move();
};


function delete_block() {
    if (!(confirm('Удалить этот блок?')))
        return
    let block = this.parentNode.parentNode.firstElementChild
    if (block.classList.contains('newpost_img')){
        let img_src = [block.querySelector('img').src]
        $.ajax({
            url: 'del_post_imgs/',
            type: 'POST',
            data: { 'src_imgs' : img_src, 'csrfmiddlewaretoken': get_cookie('csrftoken')},
        });
    }
    this.parentNode.parentNode.remove();
}
function ready_move() {//подписываем кнопки "вверх", "вниз" и "удалить" на соотвествующие события

    document.querySelectorAll(".newpost_cell_btn_blockup").forEach(block => {
        block.addEventListener("click", block_moveup)
    });
    document.querySelectorAll(".newpost_cell_btn_blockdawn").forEach(block => {
        block.addEventListener("click", block_movedawn)
    });
    document.querySelectorAll(".newpost_cell_btn_blockremove").forEach(block => {
        block.addEventListener("click", delete_block);
    });
}




document.querySelector(".new_post_new_text_btn").addEventListener("click", new_text_block);

function new_text_block() {//создаем новый блок с тестом
    if (chek_blocks_count()) {
        system_alert('Не большо 50-ти блоков');
        return
    }
    add_text_block()
    
}

function add_text_block(text = ''){
    document.querySelector('.new_post_panel_btns').insertAdjacentHTML("beforebegin", html_new_text_block(text));
    ready_move()
}

function textarea_resize(text_block){ //смена высоты textarea в зависимости от кол-ва текста пользователя
    text_block.style.cssText = 'height:auto; padding:10px';
    text_block.style.cssText = 'height:' + text_block.scrollHeight + 'px';
}

//
//Вставка изобраения ctr + v
//вдохновение
//https://www.youtube.com/watch?v=HGAPDmBA-2U
//
window.addEventListener('paste', function(e) {
    var clipboard = e.clipboardData;
    if (clipboard.files.length> 0) {
        load_images(clipboard.files)

    }
})



/*Подписываем на drag-and-drop загрузку изображений
хотел бы что бы иконка фотопарата менялась сразу при перетаскивании в окно браузера
но это работает как то через раз, да и в моем понимании этим мал окто будет пользоваться (хотя конечно будут)
В будущем вернуться бы к этому и сделать нормальное реагирование на перетескивние в окно браузера, область drop, окончание drop и т.д.
В данный момент физически оно работает и привязяно на панель кнопок, создания блоков, но визуально это не как не заметно
*/
document.addEventListener('DOMContentLoaded', () =>{
    let el = document.querySelector('.new_post_panel_btns');
    
    //фцункция загрузки 
    function onDrop(e) {
        e.preventDefault();
        load_images(e.dataTransfer.files);
        return false;
    }

    //находится над элементом сбрасывания, можно оформить в будущем и без него не работает
    function dragover_image(e) {
        e.preventDefault();
    }

    el.addEventListener('dragover', dragover_image);
    el.addEventListener('drop', onDrop)
})



//Функция вставки файлов. Получает массив файлов и загруужает их
function load_images(files) {
    for (var i = 0, f; f = files[i]; i++) {

        // Only process image files.


        if (!f.type.match('image.*')) {
            system_alert("Только изображения...");
            return
        }
        if (f.size > 11534336) {
            system_alert("Размер изображения не больше 10МБ");
            return
        }
        if (chek_blocks_count()) {
            system_alert('Не большо 50-ти блоков');
            return
        }

        var reader = new FileReader();
        // Closure to capture the file information.
        reader.onload = (function (theFile) {
            return function (e) {
                let photo_src = e.target.result;
                // let photo_alt = theFile.name; //зачем alt в конструторке???
                
                document.querySelector('.new_post_panel_btns').insertAdjacentHTML("beforebegin", html_new_img_block(photo_src));
                
                ready_move()
                ajax_load_photos(theFile, photo_src);
            };
        })(f);

        // Read in the image file as a data URL.
        reader.readAsDataURL(f);



    }
}



function new_img_block(evt) {
    //с помощью этой функции мы берем выбраные фотографии поста и выводим на страницу 
    //до начала загрузки(загрузка начинается паралельно)
    var files = evt.target.files; // FileList object

    load_images(files)

    //Ниже переустанавливаем input для фоток. Что это даетт? Пользователь может вставить одну фотку несколько раз. 
    //Не надо шаманить с files если надо удалить фотку. Достаточно удались сам блок с фоткой.
    fotos.remove();
    let new_input_photos = `<input id="fotos" name="fotos[]" class="hidden" type="file" multiple=""></input>`;
    document.querySelector('.new_post_new_fhotos_btn').insertAdjacentHTML("beforeBegin", new_input_photos);
    fotos.addEventListener('change', new_img_block);//подписываемся на событие выбора файлов для загрузки

}


fotos.addEventListener('change', new_img_block);//подписываемся на событие выбора файлов для загрузки

function delay(x) { //задержка чисто для тестов, на странице не используется(на данный момент служит для имитации загрузки фото)
    var d = new Date();
    var c, diff;
    while (1) {
        c = new Date();
        diff = c - d;
        if (diff > x) break;
    }
}

function ajax_load_photos(f, src) {//функия ajax для вставки фотографий после их загрузки
    //ищет каждую фото по ее уникальному alt и меняет ее src из локального она компьютере, на серверную
    var formData = new FormData();
    formData.append('photo', f);
    formData.append('csrfmiddlewaretoken', get_cookie('csrftoken'));

    $.ajax({
        url: 'load_photo/',
        type: 'POST',
        data: formData,
        cache: false,
        processData: false,
        contentType: false,
        success: function (response) {
            //получем от сервера ответ с новыми src картинки, после загрузки. А так же id картини в базе, для дальнейшей привязки к посту
            let new_photo = JSON.parse(response)
            //получем примерно иакой JSON ["/media/posts/2021/01/03/Logo_GJVCL8R.png", 77] и парсим его 
            document.querySelector(`img[src="${src}"]`).src = new_photo[0];
            document.querySelector(`img[src="${new_photo[0]}"]`).dataset.id = new_photo[1];
            document.querySelector(`img[src="${new_photo[0]}"]`).parentNode.querySelector('.newpost_load_photo_block').remove();
            

        }
    });



}





document.querySelector(".new_post_tags").addEventListener("keyup", function (event) {//событие при нвжвтии кнопки в нашем input тегов
    document.querySelector('.new_post_tags').value = document.querySelector('.new_post_tags').value.replace(/ ,/g, ',')

    //узнаем текущий тег
    let input_text = document.querySelector('.new_post_tags').value.trim();
    let input_text_end = input_text.lastIndexOf(',');
    if (input_text_end == -1) {
        //если запятых нет, значит вводится первый тег
        input_text_end = document.querySelector('.new_post_tags').value;
    }
    input_text = input_text.substring(input_text_end + 1).trim(); //получаем длинну текущего тега. Если есть пробел в начале, он игнорируется\
    if (input_text.length < 2) {
        if (document.querySelector('.tags_input_help_wrapper')) {
            
            document.querySelector('.tags_input_help_wrapper').remove();//удаляем подсказки, если длинна тега меньше 2-ух(например пользователь нажал backspace)
        }
        return
    }


    //действия со стрелками
    if (event.key == 'ArrowDown') {
        tags_input_help_dawn_active(this)
        tags_input_help_wrapper_scroll()
        return
    }
    if (event.key == 'ArrowUp') {
        document.querySelector(".new_post_tags").selectionStart = document.querySelector(".new_post_tags").value.length;//переносим корретку в начало input при нажатии стрелки вверх
        tags_input_help_up_active(this);
        tags_input_help_wrapper_scroll()
        return
    }
    if (event.key == 'Enter') {
        sand_tag_in_input();
        return
    }


    //конструктор/деконструктор выпадающего списка
    if (document.querySelector('.tags_input_help_wrapper') != null)
        document.querySelector('.tags_input_help_wrapper').remove();

    if (document.querySelector(".new_post_tags").value.length < 2)
        return

    var tags_data = ajax_tags_serch(input_text);
    if (!tags_data) {// проверка на tags_data == false(нет списка тегов)
        return
    }

    document.querySelector('.new_post_tags').insertAdjacentHTML("afterEnd", tags_input_help_wrapper);//создаем оболочку для списка подсказок

    let tags_input_help_cell = '';

    tags_data.forEach((value, key) => {
        tags_input_help_cell += tags_input_help_create(key, value);
    });


    document.querySelector('.tags_input_help_wrapper').insertAdjacentHTML("afterBegin", tags_input_help_cell);//вставляем варианты подсказок тегов в оболочку
    document.querySelector(".tags_input_help").classList.add('active');//выделаем первую подсказку



    //делаем подписку на события

    document.querySelectorAll(".tags_input_help").forEach(block => {
        block.addEventListener("mouseenter", tags_input_help_set_active);//делаем тег активным при наведении мышкой

    });
    document.querySelectorAll(".tags_input_help").forEach(block => {
        block.addEventListener("click", sand_tag_in_input);//добвляем тег в input при клике
    });

    set_tags_input_help_count();
    tags_input_help_wrapper_scroll()




});

function all_tags_input_help_unset_active() {
    document.querySelectorAll('.tags_input_help.active').forEach(block => {
        block.classList.remove('active');
    })
}

function tags_input_help_wrapper_scroll() {//автопрокрутка до выделенной подсказки
    var top_distanse = document.querySelector('.tags_input_help.active');
    if (top_distanse == null)//если не нашли выделеный пункт подсказок, прервали автопрокрутку, т.к. крутить не к чему
        return
    var top_distanse = top_distanse.offsetTop;
    var perent_hegt = document.querySelector('.tags_input_help_wrapper').clientHeight / 2;
    document.querySelector('.tags_input_help_wrapper').scrollTop = top_distanse - perent_hegt;
}

//расчет и изменени/возврат количества тегов-подсказок со счетом нуля. Что бы было легче работать с массивом
var tags_input_help_count
function set_tags_input_help_count() {
    tags_input_help_count = document.querySelectorAll('.tags_input_help').length - 1;
    return tags_input_help_count;
}

function tags_input_help_set_active() {//даем тегу выделение (вызывается при наведении мышкой)
    all_tags_input_help_unset_active();
    this.classList.add('active');
}




function tags_input_help_up_active() {//переносим выделение на один блок вверх(вызывается при нажатии стрелки вверх) 
    let active_block = document.querySelector(".tags_input_help.active");
    let active_block_number = serch_block_index('tags_input_help', active_block)
    if (active_block_number == 0) {//если блок верхний, выделяем нижний
        document.querySelector('.tags_input_help.active').classList.remove('active');
        document.querySelectorAll('.tags_input_help')[tags_input_help_count].classList.add('active');
        return
    }
    document.querySelector('.tags_input_help.active').classList.remove('active');
    document.querySelectorAll('.tags_input_help')[active_block_number - 1].classList.add('active');

}
function tags_input_help_dawn_active() {//переносим выделение на один блок вниз(вызывается при нажатии стрелки вниз) 
    let active_block = document.querySelector(".tags_input_help.active");
    let active_block_number = serch_block_index('tags_input_help', active_block);
    if (active_block_number == set_tags_input_help_count()) {//если блок нижний, выделяем верхний
        document.querySelector('.tags_input_help.active').classList.remove('active');
        document.querySelectorAll('.tags_input_help')[0].classList.add('active');
        return
    }

    document.querySelector('.tags_input_help.active').classList.remove('active');
    document.querySelectorAll('.tags_input_help')[active_block_number + 1].classList.add('active');

}

function sand_tag_in_input() {//вставляем выбраный пункт из списка


    let select_tag = document.querySelector('.tags_input_help.active').querySelector('.tags_input_help_tag').textContent;
    
    
    let entered_tags_list_without_last = tags_constructor()//берем массив уже введеных тегов
    entered_tags_list_without_last.pop()  //удаляем тег, вводимый сейчас
    if (entered_tags_list_without_last.indexOf(select_tag.toLowerCase()) > -1) {
        system_alert('Нелья повторять теги')
        return
    }

    let input_text = document.querySelector('.new_post_tags').value.trim();

    select_tag += ', ';
    let input_text_end = input_text.lastIndexOf(',');
    if (input_text_end == -1) {
        document.querySelector('.new_post_tags').value = select_tag;
        document.querySelector('.tags_input_help_wrapper').remove();
        return
    }
    input_text = input_text.slice(0, (input_text_end + 1));
    document.querySelector('.new_post_tags').value = input_text + ' ' + select_tag;
    document.querySelector('.tags_input_help_wrapper').remove();
}

function ajax_tags_serch(min_tag) {//получем часть input посылаем его на сервер, он возвращает схожие теги и количество постов с ними, возвращаем этот список тегов + кол-во постов
    var server_data = {}
    request = { 'csrfmiddlewaretoken': get_cookie('csrftoken'), 'tag': min_tag }


    $.ajax({
        type: 'POST',
        url: 'tags_serch/',
        data: request,
        async: false,
        success: function (response) {
            server_data = response;
        }
    })


    if (Object.keys(server_data).length == 0) {
        return false
    }
    let data = new Map();

    for (var key in server_data) {//делаем первые буквы заглавными
        new_key = key[0].toUpperCase() + key.slice(1);//делаем первую букву ключа заглавной
        data.set(new_key, Number(server_data[key]));
    }
    return data
}

function name_post_cheker(post_name) {
    let name_length = post_name.match(/[A-Za-zА-яа-я]/g);
    if (name_length == null)
        return true
    name_length = name_length.length;
    if ((name_length < 5) || (name_length > 120))
        return true
}

function post_cell_cheker(cells) {

    if (Object.keys(cells).length < 1)
        return true
}

function tags_checker(tags) {
    if (tags.length < 2) {
        system_alert("не меньше 2-x тегов");
        return true;
    }
    if (tags.length > 20) {
        system_alert("не меньше 20-ти тегов");
        return true;
    }
}

function name_post_constructor() {
    return document.querySelector(".newpost_name").value;
}


function post_content_constructor() {
    let out_data = {};
    let block_count = 0
    document.querySelectorAll('.newpost_blok').forEach(block => {
        //если блок с текстом
        if (block.querySelector('.newpost_text')) {
            let block_text = block.querySelector('.newpost_text').value;
            if (block_text == '')
                return
            out_data[`_${block_count}_text`] = block_text;
            block_count++
            return
        }
        //если болок с картинкой
        if ((block.querySelector('.newpost_img'))) {
            
            let img_data = block.querySelector('.newpost_img img').src;
            out_data[`_${block_count}_img`] = img_data;
            block_count++
            return
        }
        //разбор блоков с видео
        //многие функции и перменные в соседнем файле add_video.js
        if ((block.querySelector('.newpost_video'))) {
            
            let is_type_found = false
            let iframe_src = block.querySelector('.newpost_video iframe').src
            if (try_get_youtube_id (iframe_src)){
                is_type_found = true           
            }
            if (try_get_coub_id (iframe_src)){
                is_type_found = true           
            }
            if(is_type_found){
                
                out_data[`_${block_count}_video_${type_video}`] = video_id;
                block_count++
            }
           
            return
        }


    });
    return out_data;
}


function tags_constructor() {
    let tagsgroup = document.querySelector('.new_post_tags').value.split(',');
    
    for (let i = 0; i < tagsgroup.length; i++) {
        if (tagsgroup[i].trim().length < 3) {
            tagsgroup.splice([i], 1);
            i--
            continue
        }
        tagsgroup[i] = tagsgroup[i].trim().toLowerCase();
        
    }

    for (let i = 0; i < tagsgroup.length; i++) {//запускаем второй фильтрующий массив, для двойных запятых
        if (tagsgroup[i].trim().length < 3) {
            tagsgroup.splice([i], 1);
            i--
            continue
        }
    }
    //проверяем теги на количество символов
    

    return tagsgroup
}


function main_tagsgroup_constructor() {
    let main_tagsgroup = [];
    test = document.querySelector('.newpost_tagsgroup').querySelectorAll('input').forEach(block => {
        if (block.checked)
            main_tagsgroup.push(block.value);
    });
    return main_tagsgroup;
}

function del_dublekate(array) {
    let result = [];

    for (let str of array) {
        if (!result.includes(str)) {
            result.push(str);
        }
    }

    return result;
}



document.querySelector('.publish').addEventListener("click", () => {

    let newpost_name = document.querySelector('.newpost_name').value;
    let full_post_data = {};
    full_post_data['name_post'] = name_post_constructor();
    full_post_data['post_content'] = post_content_constructor();
    full_post_data['tags'] = tags_constructor();
    full_post_data['main_tags'] = main_tagsgroup_constructor();

    let main_tags_list = ['nsfw', 'политика', 'жесть', 'мое'];
    let duble_main_tags = false;

    for (let i = 0; i < full_post_data['tags'].length; i++) {//проверяем совпадения обычных тегов с главными
        if (main_tags_list.indexOf(full_post_data['tags'][i]) > -1) {
            full_post_data['tags'].splice([i], 1);
            duble_main_tags = true;
        }

    }



    if (duble_main_tags) {//если было совпадение, переписываем инпут
        document.querySelector('.new_post_tags').value = full_post_data['tags'].join(', ')
        full_post_data['tags'] = tags_constructor();
        if (full_post_data['tags'].length < 3) {//если после переписи осталось меньше 3-х тегов
            system_alert('Теги: "nsfw", "политика", "жесть", "мое" ставятся отдельно')
            return
        }
    }

    if (del_dublekate(full_post_data['tags']).length != full_post_data['tags'].length) {
        system_alert('Теги не должны повторяться');
        return;
    }

    if (name_post_cheker(full_post_data['name_post'])) {
        system_alert('Название поста от 5 до 120 букв');
        return;
    }
    if (post_cell_cheker(full_post_data['post_content'])) {
        system_alert('Нелья отправлять пустой пост');
        return;
    }
    if (tags_checker(full_post_data['tags'])) {
        return;
    }
    full_post_data = JSON.stringify(full_post_data);
    
    

    tkn = document.querySelector('input[name="csrfmiddlewaretoken"]')

    form = new FormData();
    form.append('post', full_post_data)
    form.append('csrfmiddlewaretoken', tkn.value)

    $.ajax({

        type: 'POST',
        url: 'save_post/',
        cache: false,
        processData: false,
        contentType: false,
        data: form,
        success: function (response) {
            if(check_server_errors(response)){
                return
            }
            //Если пост сохранился, 
            del_from_local_storage()
            bool_del_local_storage = false //меняем переменную что бы куки не записали при уходе со страницы
            window.location.href = `/post/${response}`; //перенаправляем на новый пост
        }
    });


});

function del_from_local_storage() {
    localStorage.removeItem('raw_user_post')//удаляем из local storage
}

//
//
//Сборка и записываение поста в local storage
//
//
function set_post_local_storage(){
    del_from_local_storage()

    let full_post_data = {};
    full_post_data['name_post'] = name_post_constructor();
    full_post_data['post_content'] = post_content_constructor();
    full_post_data['tags'] = tags_constructor();
    full_post_data['main_tags'] = main_tagsgroup_constructor();
    
    full_post_data = JSON.stringify(full_post_data)
    
    localStorage.setItem('raw_user_post', full_post_data)
}




//предпросмотр поста
preview_post_btn.addEventListener('click', () => {
    set_post_local_storage()
    window.open('new_post_preview/');//открываем в новой вкладке
})


//обнуление поста
nullify_post_btn.addEventListener('click', () => {
    //удаляем фотографии
    let img_src_list = []
    document.querySelectorAll('.newpost_img img').forEach( block_img =>{
        img_src_list.push(block_img.src);
    })

    $.ajax({
        url: 'del_post_imgs/',
        type: 'POST',
        data: { 'src_imgs' : img_src_list, 'csrfmiddlewaretoken': get_cookie('csrftoken')},
    });

    //меняем переменную что бы содержимое удалилось
    bool_del_local_storage = false
    location.reload();//обновляемся
})

//Сохраняем или удаляем перед закрытием
window.onbeforeunload = ()=>{
    if(bool_del_local_storage){
        set_post_local_storage()
    }
    else{
        del_from_local_storage()
    }
}

//
//
// Вывод данных поста из local storage если такой есть
//
//
document.addEventListener('DOMContentLoaded', load_post_from_local_storage)

function load_post_from_local_storage(){
    
    let post_data = localStorage.getItem('raw_user_post')
    if (post_data == null){//проверка на в принипе существование записей о посте
        return
    }
    post_data = JSON.parse(post_data)

    document.querySelector('.newpost_name').value = post_data.name_post 
    post_content_parese(post_data.post_content)
    post_tags_parse(post_data.tags)
    post_main_tags_parse(post_data.main_tags)

}

//контструктор контента поста
function post_content_parese(post_content){

    for (key in post_content){
        // one_cell_post_content == post_content[key]
        //если у нас текст
        if (key.indexOf('_text') != -1){
            add_text_block(post_content[key])
        }
        //если у нас картинка
        if (key.indexOf('_img') != -1){
            add_img_block(post_content[key]) 
        }
        //если блок с ютубом
        if (key.indexOf('_video_youtube') != -1){
            type_video = 'youtube'
            video_id = post_content[key]
            select_block_video()
        }
        //если блок с кубом
        if (key.indexOf('_video_coub') != -1){
            type_video = 'coub'
            video_id = post_content[key]
            select_block_video()
        }

    }
    ready_move()//подписываем кнопки

}

function add_img_block(src) {
    document.querySelector('.new_post_panel_btns').insertAdjacentHTML("beforebegin", html_new_img_block(src, true));
}

//вставляем теги в input
function post_tags_parse(tags_list) {
    let tags_input = document.querySelector('.new_post_tags')
    for (i in tags_list){
        if (tags_list[i].length < 2){//без этого вконце будет лишняя запятая
            continue
        }
        tags_input.value += tags_list[i] + ', '
    }
}

//расставляем галочки main тегов
function post_main_tags_parse(main_tags_list) {
    for (i in main_tags_list){
        document.querySelector(`input[value="${main_tags_list[i]}"]`).checked = true

    }
}


