/*Модальное окно и его основные функции*/

// window.onload = show_modal_window



const modal_window = document.querySelector('.modal_window_wrapper')
const fone_modal_window = document.querySelector('.modal_window_fone')
const modal_window_text_header = modal_window.querySelector('.modal_window_heading')
const modal_window_HTML_body = modal_window.querySelector('.body_modal_window')
const message_block = modal_window.querySelector('.message_modal_window')

//Функция вывода модального окна
function show_modal_window(text_header = '', HTML_conent = '') {
    fone_modal_window.classList.add('window_fone_open')
    
    back.classList.add('lock');//запрещаем прокрутку body

    modal_window_text_header.textContent = text_header
    modal_window_HTML_body.innerHTML = HTML_conent

    setTimeout(()=>{
        modal_window.classList.add('modal_window_open')
    }, 10)
   
}

//Функция скрытия модального окна
function hide_modal_window() {
    modal_window.classList.remove('modal_window_open')
    back.classList.remove('lock');//разрешаем прокрутку body

    setTimeout(()=>{
        fone_modal_window.classList.remove('window_fone_open')
        
    
    }, 200)

    setTimeout(()=>{//отчищаем модальное окно
        modal_window_text_header.textContent = ''
        modal_window_HTML_body.innerHTML = '' 
        clear_modal_window_message() 
    }, 1)
}

//Выводим сообщения об ошибке
function message_modal_window(message_text = '') {
    document.querySelector('.message_modal_window').textContent = message_text
}

function clear_modal_window_message(){
    message_block.textContent = ''  

}