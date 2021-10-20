from django.contrib import admin
from .models import Post, Categories, Comments, PostCategory, Author

def nullRating(modeladmin, request, queryset):
    queryset.update(post_rating = 0)
nullRating.short_description = 'Set rating 0'

class PostAdmin(admin.ModelAdmin):
    list_display = ('post_title', 'id', 'post_date', 'post_rating', 'author')
    list_filter = ('id', 'post_date', 'post_rating')
    search_fields = ('post_title', 'author__user__username')
    actions = [nullRating]

class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'id', 'comment_rating', 'comment_datetime')
# Register your models here.

admin.site.register(Post, PostAdmin)
admin.site.register(Comments,CommentAdmin)
admin.site.register(Categories)
admin.site.register(PostCategory)
admin.site.register(Author)