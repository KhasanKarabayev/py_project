from django.contrib import admin
from .models import Category, Post


class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'watched', 'is_published', 'category', 'created_at', 'updated_at']
    list_display_links = ['id', 'title']
    list_editable = ['is_published']
    readonly_fields = ['watched']
    list_filter = ['title', 'category', 'watched']


admin.site.register(Category)
admin.site.register(Post, PostAdmin)
