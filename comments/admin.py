from django.contrib import admin
from .models import Comment, CommentLike


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['content_preview', 'article', 'user', 'parent', 'is_edited',
                    'is_deleted', 'likes_count', 'created_at']
    list_filter = ['is_edited', 'is_deleted', 'created_at']
    search_fields = ['content', 'user__username', 'article__title']
    readonly_fields = ['likes_count', 'created_at', 'updated_at', 'replies_count_display']
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Информация', {
            'fields': ('article', 'user', 'parent')
        }),
        ('Содержание', {
            'fields': ('content',)
        }),
        ('Статус', {
            'fields': ('is_edited', 'is_deleted')
        }),
        ('Статистика', {
            'fields': ('likes_count', 'replies_count_display', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Комментарий'

    def replies_count_display(self, obj):
        return obj.replies_count()
    replies_count_display.short_description = 'Количество ответов'


@admin.register(CommentLike)
class CommentLikeAdmin(admin.ModelAdmin):
    list_display = ['comment', 'user', 'created_at']
    search_fields = ['comment__content', 'user__username']
    list_filter = ['created_at']
    date_hierarchy = 'created_at'
    readonly_fields = ['comment', 'user', 'created_at']

    def has_add_permission(self, request):
        return False
