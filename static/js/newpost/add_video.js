document.querySelector('.new_post_new_video_btn').addEventListener('click', start_add_video)


const add_video_window_header = 'Вставте ссылку на YouTube или Coub'
const add_video_window_HTML = `<input class="add_video_input" type="text">

                               <div class="button_video_input">Добавить</button>`

var video_id    //id видео на сторонем сайте
var type_video  //тип сайта на котором видео

//вызываем окно и обрабатываем кнопку "добавить"
function start_add_video() {
    show_modal_window(add_video_window_header, add_video_window_HTML);
    document.querySelector('.button_video_input').addEventListener('click', add_video)
}


//берем url, достаем id видео и узнаем его тип ютуб или куб
function add_video() {
    clear_modal_window_message()//отчищаем сообщения об ошибках
    let raw_url_string = document.querySelector('.add_video_input').value

    if (try_get_youtube_id (raw_url_string)){
        select_block_video()
        hide_modal_window()
        return
    }
    if (try_get_coub_id (raw_url_string)){
        select_block_video()
        hide_modal_window()
        return
    }
    message_modal_window('Не удалось распознать ссылку')    
}

//пробуем достать id видео с youtube, если получается, устанавливаем глобальные переменные
function try_get_youtube_id (raw_url_string){
    let regExp = /^.*(youtu\.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=)([^#\&\?]*).*/;
    let match = raw_url_string.match(regExp);
    if (match && match[2].length == 11) {
        video_id = match[2]
        type_video = 'youtube'
        return true

    } else {
        return false
    }
}

//пробуем достать id видео с coub, если получается, устанавливаем глобальные переменные
function try_get_coub_id (raw_url_string){
    let regExp = /(\/coub.com\/[^\s]*\/)([^\s]*)/;
    let match = raw_url_string.match(regExp);
    if (match){
        video_id = match[2]
        type_video = 'coub'
        return true
    }
    else{
        return false
    }
}


//принимаем тип видео и в зависимости от него, добавляем блок
function select_block_video() {
    let HTML_iframe = ``
    if (type_video == 'youtube'){
        console.log('узнали ютуб, кго id ' + video_id);
        HTML_iframe = get_iframe_youtube(video_id)
        add_block_video(HTML_iframe)
       

    }
    if (type_video == 'coub'){
        HTML_iframe = get_iframe_coub(video_id)
        add_block_video(HTML_iframe)
    }
    
}

//Получаем HTML iframe видео и встваляем его добавляя все остальное для блока конструктора
function add_block_video(vieo_wrapper_HTML) {
    // ${get_buttoms()}

   let block_html = `<div class="newpost_cell newpost_blok">
                        <div class="temp_class_1 newpost_video"> 
                           ${vieo_wrapper_HTML}
                            
                        </div>
                        ${get_buttoms()}
                    </div>`
    
    document.querySelector('.new_post_panel_btns').insertAdjacentHTML("beforebegin", block_html);
    ready_move()

}

function get_iframe_youtube(video_id){
    return `<iframe 
                width="100%" 
                height="350" 
                src="https://www.youtube.com/embed/${video_id}" 
                title="YouTube video player"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                frameborder="0"  allowfullscreen>
            </iframe>`
}

function get_iframe_coub(video_id){

    return `<iframe 
              width="100%" 
              height="350"  
              src="https://coub.com/embed/${video_id}" 
              title="Coub video player"
              allowfullscreen 
              allow="autoplay"
              frameborder="0" >
            </iframe>`
}