from django.contrib import admin
from .models import Posts, CustomUser, Comments, AdminMessages, Tags

class TagPostsInline(admin.TabularInline):
    '''Класс для связи и редкактирования тегов поста по обратной связи ManyToMany'''
    model = Posts.tags_set.through
    extra = 1


class PostsAdmin(admin.ModelAdmin):
    
    list_display = ('id', 'author', 'name', 'post_rating', 'views', 'deleted',  'date_create')
    list_display_links = ('id','name')
    search_fields = ('id', 'name', 'content', 'date_create')
    inlines = [TagPostsInline]

    def deleted(self, obj):
        if (hasattr(obj, 'deletedposts')):
            return 'Да'
        return 'Нет'
    deleted.short_description = 'Удален'
    

class CustomUserAdmin(admin.ModelAdmin):
    
    list_display = ('id', 'username', 'first_name', 'user_rating', 'group', 'email', 'date_joined')
    list_display_links = ('id','username')
    search_fields = ('id', 'name', 'group')

    
    def user_rating(self, obj):
        return obj.profile.user_rating
    user_rating.short_description = 'user_rating'


class CommentsAdmin(admin.ModelAdmin):
    
    list_display = ('id', 'post_id', 'user_id', 'perent_comment_id', 'comment_rating', 'deleted', 'date_create')
    list_display_links = ('id', 'post_id', 'user_id')
    search_fields = ('id', 'post_id', 'user_id', 'content')

    def deleted(self, obj):
        if (hasattr(obj, 'deletedcomments')):
           return 'Да'
        return 'Нет'
    deleted.short_description = 'Удален'

class AdminMessagesAdmin(admin.ModelAdmin):
    
    list_display = ('name', 'text', 'user_username', 'date_create')
    # list_display_links = ('id', 'user_id', 'name')
    # search_fields = ('id', 'user_username', 'name')

    def user_username(self, obj):
        if obj.user_id.username == None:
            return ' '
        return obj.user_id.username
    user_username.short_description = 'user_rating'

class AdminTags(admin.ModelAdmin):

    list_display = ('tag', 'count_posts', )
    list_display_links = ('tag', 'count_posts')
    search_fields = ('tag', 'count_posts')
    raw_id_fields = ("posts",)
   
    

admin.site.register(Posts, PostsAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Comments, CommentsAdmin)
admin.site.register(AdminMessages, AdminMessagesAdmin)
admin.site.register(Tags, AdminTags)