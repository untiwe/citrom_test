
chek_options()//т.к. стоит послденим, не надо привязывать к событям

document.querySelectorAll('.search_option').forEach(element =>{
    element.addEventListener('change', chek_options)
});

//проверка всех чекбоксов и придание стиля их label в зависимости от изменения
function chek_options() {
    document.querySelectorAll('.search_option').forEach(element =>{
        
        if (element.checked){
            element.labels[0].classList.add('button_active');
            }
        else{
            element.labels[0].classList.remove('button_active');
            }   
        
    });
}
    

function ajax_load_content() {
//get_request это строковая вариация GET запроса, ее прописывает сервер
    let options = get_request.replace(/&amp;/g, '&');
    
    var posts = null
    $.ajax({
        type: 'GET',
        url: 'searchlist/' + options,
        async: false,
        data: { 'page': page_number },
        success: function (response) {
            posts = response;
        }
    });
    page_number += 1
    return JSON.parse(posts)
}