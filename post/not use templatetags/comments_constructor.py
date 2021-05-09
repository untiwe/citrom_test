from django import template
# https://www.youtube.com/watch?v=BKUYxMKa5dw&list=PLrgHtaQ10vi3xalWI7q6Uzr7aZUNT0BJH&index=20

register = template.Library()  # регистрируем тег


@register.inclusion_tag("post/child_comment.html", takes_context=True)
def show_child_comments(context, peretnt_comment_id=0):
    all_comments = context["comments"]
    child_comments = []
    print(all_comments)
    for i in range(all_comments.count()):
        print('%s and %s' % (peretnt_comment_id,
                             all_comments[i].perent_comment_id))
        if peretnt_comment_id == all_comments[i].perent_comment_id:
            child_comments.append(all_comments[i])

    if not child_comments:
        return None
    return {"comments": child_comments}
