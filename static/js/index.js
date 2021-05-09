//Сворачиваем посты после полной загрузки страницы
// window.addEventListener("load", function (event) {
//     post_content_uncover()
// });


//запрпос на загрузку постов, возвращает HTML
function ajax_load_content() {
    views_post_list = localStorage.getItem('views_posts')
    if (views_post_list != null) {
        views_post_list = views_post_list.split(',');
    }
    var posts = null
    $.ajax({
        type: 'POST',
        url: 'new_page_posts/',
        async: false,
        data: { 'page': page_number, 'csrfmiddlewaretoken': get_cookie('csrftoken'), 'views_posts': views_post_list },
        success: function (response) {
            posts = response;
        }
    });
    console.log(page_number);
    page_number += 1
    return JSON.parse(posts)
}
