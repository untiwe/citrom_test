//Вызов некоторых функций вшит в HTML и он срабатывает до загрузки остального js. Эта библиотека вставлена в начало документа, что бы небыло ошибок при загрузке страницы


//функция сворачивания постов, если такая подключена
function try_post_content_uncover() {
    //делаем проверку что бы в ее отсутсвие небыло ошиблок
    if(typeof post_content_uncover == 'function'){
        post_content_uncover();
    }
}