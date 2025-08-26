from django.contrib import admin
from .models import Comment

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'post', 'created_at', 'is_active', 'rating']
    list_filter = ['is_active', 'created_at', 'rating']
    search_fields = ['author__username', 'post__name', 'text']
    list_editable = ['is_active']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
