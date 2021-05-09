function post_content_uncover() {//метод "сворачивания" постов, если таковые есть. Каждый раз при вызове, обходить все классы .post_content на странице
document.querySelectorAll('.post_content').forEach(post_content_wrapper => {
        
        if (post_content_wrapper.getElementsByClassName('post_scroll_button').length == 1)
            return

        if (post_content_wrapper.scrollHeight > 900) {

            post_content_wrapper.style.height = "600px";
            post_content_wrapper.innerHTML += "<div class='post_scroll_button'  onclick='post_cover(this)' >Развернуть</div>";
        }
    });
}


function post_cover(post_content_wrapper) {//сворачиваем или разворачиваем пост
    if (post_content_wrapper.parentNode.style.height == "600px") {
        post_content_wrapper.parentNode.style.height = '';
        post_content_wrapper.parentNode.style.paddingBottom = '30px';
        post_content_wrapper.textContent = 'Свернуть';
    }
    else {
        post_content_wrapper.parentNode.style.height = "600px"
        post_content_wrapper.parentNode.style.paddingBottom = '0';
        post_content_wrapper.textContent = 'Развернуть';
    }

}
