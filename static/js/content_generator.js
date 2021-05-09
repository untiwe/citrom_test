/*Эта JS подкючется на всех страницах, где есть генерация постов, комментариев, сообщений и т.д. (index/user/search)
На каждой странице, в ее библиотете, надо определить function ajax_load_content с учетом особеностей страницы. Которая возвращет JSON поста и тут он парсится.
Так же может быть вызов события подгрузки у коментаривев и др. В этом случае ajax_load_content так же вызывается но в этом слчуае на каждой странице долен быть не только правильный
вызов JSON но так же реализация контета и его вставка на страницу. Сам ajax_load_content в этом случае возвращает null и цикл отрисвки посто здесь не запускается*/

//конструктор HTML одного поста
function post_generator(post){
    let post_content = `
    <article class="post">
        
        <div class="post_name_wrapper">
            <h2 class="post_name"><a href="${href_post(post.post_id)}">${post.name}</a></h2>
            ${may_change(post.may_change)}
            
        </div>
        <section class="post_content">
        <span class="post_tags">${construct_post_tasg(post.tags)}</span>
            ${check_is_deleted(post.is_deleted)}
            ${construct_post_content(post.content)}
        </section>
        <section class="post_footer" data-post="${post.post_id}">
            <a href="${href_user(post.author)}" class="post_footer_cell post_avatar"><img src=${post.avatar} alt="аватар"></a>
            <a href="${href_user(post.author)}" class="post_footer_cell post_author">${post.author}</a>
            <div class="post_footer_cell post_footer_img_wrapper post_dawn_arrow" onclick="eval_post(this.parentNode, false)">
                <img class="post_img_footer" src="${construct_post_dawn_arrow(post.eval)}" alt="плохая оценка">
            </div>
            <div class="post_footer_cell post_count_score">${post.rating}</div>

            <div class="post_footer_cell post_footer_img_wrapper post_dawn_arrow" onclick="eval_post(this.parentNode, true)">
                <img class="post_img_footer" src="${construct_post_up_arrow(post.eval)}" alt="плохая оценка">
            </div>

            <div class="post_footer_cell pass"></div>

            <div class="post_footer_cell post_count_viwes">${post.views}</div>

            <div class="post_footer_cell post_footer_img_wrapper post_eve">
                <img class="post_img_footer" src="../../static/img/eve.svg" alt="картинка просмотров">
            </div>

            <div class="post_footer_cell post_count_comments">${post.comments}</div>

            <a href="${href_post(post.post_id)}" class="post_footer_cell post_footer_img_wrapper post_img_comments">
                <img class="post_img_footer" src="../../static/img/message.svg" alt="картинка коментариев">
            </a>
        </section>
    </article>`;
    
    return post_content

}


function construct_post_content(content){
    let html_out = '';
    for (key in content){
        if(key.indexOf  ('_text') != -1){
            html_text = convert_links(content[key])//оборачиваем ссылки
            html_text = add_br_text(html_text)
            html_out += `<p class="post_content_cell">${html_text}</p>`
            continue
        }
        if (key.indexOf('_img') != -1){
            html_out += `
            <p class="post_content_cell">
                <div class="post_content_cell_img_wrapper">
                    <img onclick="expand_picture(this.src)" onload="try_post_content_uncover()" src="${content[key]}" alt="Картинка к посту">
                </div>
            </p>`
            continue
        }
        if (key.indexOf('_video_youtube') != -1){
            html_out += `
                        <p class="post_content_cell">
                            <iframe 
                                width="100%" 
                                height="400" 
                                src="https://www.youtube.com/embed/${content[key]}" 
                                title="YouTube video player"
                                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                                frameborder="0"  allowfullscreen>
                            </iframe>
                        </p>`
            continue
        } 
        if (key.indexOf('_video_coub') != -1){
            html_out += `
                        <p class="post_content_cell">
                            <iframe 
                                width="100%" 
                                height="400"  
                                src="https://coub.com/embed/${content[key]}" 
                                title="Coub video player"
                                allowfullscreen 
                                allow="autoplay"
                                frameborder="0" >
                            </iframe>
                        </p>`
            continue
        } 
    }
    return html_out;
}

function construct_post_tasg(tags){
    let html_out = '';
    for (i in tags){
        html_out += `<a href="/search/?tag=on&key=${tags[i]}" class="post_one_tag">${tags[i]}</a>`
    }
    return html_out;
}

function construct_post_dawn_arrow(eval){
    if (eval == -1){
       return big_dislike_eval_src
    }
    else{
        return big_dawn_neutral_eval_src
    }
}
function construct_post_up_arrow(eval){
    if (eval == 1){
       return big_like_eval_src
    }
    else{
        return big_up_neutral_eval_src
    }
}

//Если may_change = true пользователь может изменать этот пост
function may_change (may_change){
    if (may_change){
        return `<img class="post_name_img" onclick="delete_post(this)" src="../../static/img/delete_icon.svg" alt="удалить пост">`
    }
    else{
        return ``
    }
}

function check_is_deleted(is_deleted){
    if (is_deleted){
        return `<div class="post_content_cell del_message">Пост удален</div>`
    }
    else{
        return ``
    }

}



//
//
//
//Постраничная загрузка постов через ajax 
//
//
var page_number = 1
var block_for_scroll = document.querySelector('.block_for_scroll')//выбираем блок, при виде которого будет вызываться событие(вешаем событие ниже)
var content_counter = 0
document.addEventListener('DOMContentLoaded', load_content);
function load_content() {

    clear_content_message()//убираем сообщения о конце контента (их может и не быть, но ошибки не будет)
    let content = ajax_load_content();
    let scope = document.querySelector('.page_content_wrapper');
    let object_in_page = 5//объектов на странице, постов 5, сообщений и коментариев 10
    
   
    if (content == 'post_comments'){
        return //если есть 'post_comments' значит на странице поста, и событие для комментариев. Подписываться не надо, т.к. коментарии загружаются разом
    }
    else if(content['not_posts'] == undefined){ //если пришли посты, вставляем  их
        for (key in content) {
            let one_post = post_generator(content[key]);

            
            scope.insertAdjacentHTML("beforeend", one_post);

            content_counter++
            
        }
        
        if (content_counter == 5)
    
        views_counter();//подписываем посты на счетчик просмотров после вставки
        
    }
    else{
        content = content['not_posts'] // или убираем ключь объекта. Что бы считать конец контента не зависимо от его типа
        object_in_page = 10

    }
    

    //page_number меняется каждым ajax запросом, кторый заправшивает новый контент и сразу после него +1 по этому после ajax_load_content() page_number равная как минимум 2


    let length_content = Object.keys(content).length; //количество элементов в ответе
    if (length_content < object_in_page) { //если элементов меньше кол-ва на одну страницу
        if (length_content > 0 || page_number > 2){ // если элементов больше 0 или страница не первая (ну тоесть вторая) значит элементы для вывода кончились
            end_conetnt_message();
            unsub_observer_page();
        }
        else{ // "или" значит что пришло 0 элиментов с первой же (ну тоесть второй) ситраницы и выводить вообще нечего
            no_conetnt_message();
        }
        
        
    }
    //если страница первая(ну тоесть вторая) и пришло максимальное количесвто элементов, значит можно загрузить что то еще, тут мы и подписываемся на контент
    if (length_content == object_in_page && page_number == 2 ){ //tckb
        sub_observer_page();//подписываемся на обновление контектна
    }

};




//создаем наблюдатель, кторый вызывает подгрузку постов при надобности
// window.addEventListener('load', sub_observer_page);

var observer_page_options = {       // устанавливаем настройки
    root: null,         // родитель целевого элемента - область просмотра=
    rootMargin: '0px',  // без отступов=
    threshold: 1      // процент пересечения
    }

// создаем наблюдатель
var observer_page = new IntersectionObserver((entries, observer) => {
    
        if (entries[0].isIntersecting) {
            //загружаем посты 
            load_content();
            
        }  

}, observer_page_options)

//подписка на observer, т.е. на догрузку контента
function sub_observer_page() { 
    observer_page.observe(block_for_scroll)
}
//отписка от observer
function unsub_observer_page() { 
    observer_page.unobserve(block_for_scroll)
}
