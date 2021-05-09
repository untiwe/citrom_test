//
//
// Вывод данных поста из local storage если такой есть
//
//
document.addEventListener('DOMContentLoaded', load_post_from_local_storage)

function load_post_from_local_storage(){
    
    let post_data = localStorage.getItem('raw_user_post')
    post_data = JSON.parse(post_data)
    if (post_data.name_post != null){
        document.querySelector('.post_name').textContent = post_data.name_post
    }
    post_tags_parse(post_data.tags)
    post_tags_parse(post_data.main_tags)
    post_content_parese(post_data.post_content)

}

//контструктор контента поста
function post_content_parese(post_content){

    for (key in post_content){
        //если у нас текст
        if (key.indexOf('_text') != -1){
            add_text_block(post_content[key])
        }
        //если у нас картинка
        if (key.indexOf('_img') != -1){
            add_img_block(post_content[key]) 
            
        }
        if (key.indexOf('_video_youtube') != -1){
            add_youtube_block(post_content[key])
        }
        if (key.indexOf('_video_coub') != -1){
            add_coub_block(post_content[key])
        }
    }

}

function add_text_block(content) {

    content = escape_text(content) //экранируем html
    content = add_br_text(content) //добавляем переносы
    let HTML_content = `<p class="post_content_cell">${content}</p>`
    add_post_content_сell_block(HTML_content)

    
}

function add_img_block(src) {
    let HTML_content = `<div class="post_content_cell_img_wrapper">
                            <img src="${src}" alt="Картинка к посту">
                        </div>`
    add_post_content_сell_block(HTML_content)

}

function add_youtube_block(video_id) {
    let HTML_content = `<p class="post_content_cell">
                            <iframe 
                                width="100%" 
                                height="400" 
                                src="https://www.youtube.com/embed/${video_id}" 
                                title="YouTube video player"
                                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                                frameborder="0"  allowfullscreen>
                            </iframe>
                        </p>`
    add_post_content_сell_block(HTML_content)
}

function add_coub_block(video_id) {
    let HTML_content = `<p class="post_content_cell">
                            <iframe 
                                width="100%" 
                                height="400"  
                                src="https://coub.com/embed/${video_id}" 
                                title="Coub video player"
                                allowfullscreen 
                                allow="autoplay"
                                frameborder="0" >
                            </iframe>
                        </p>`
add_post_content_сell_block(HTML_content)

}

//вставляем теги
function post_tags_parse(tags_list) {
    let tags_wrapper = document.querySelector('.post_tags')
    console.log(tags_wrapper);
    for (i in tags_list){
        if (tags_list[i].length < 2){//пропускаем пустые тэги
            continue
        }
        let HTML_tag = `<a href="/search/?tag=on&amp;key=${tags_list[i]}" class="post_one_tag">${tags_list[i]}</a>`
        tags_wrapper.insertAdjacentHTML('beforeend', HTML_tag)
    }
}



function add_post_content_сell_block(HTML_content) {
    let tag_block = document.querySelector('.post_content')
    tag_block.insertAdjacentHTML("beforeend", HTML_content)
}


// function post_main_tags_parse(main_tags_list) {
//     for (i in main_tags_list){
//         document.querySelector(`input[value="${main_tags_list[i]}"]`).checked = true

//     }
// }