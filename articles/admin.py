from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Tag, Article, ArticleView, Reaction


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['icon_preview', 'name', 'slug', 'color_display', 'article_count', 'order', 'created_at']
    list_editable = ['order']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['order', 'name']
    readonly_fields = ['icon_image_preview']

    fields = ['name', 'slug', 'description', 'icon', 'icon_image', 'icon_image_preview', 'color', 'order']

    def icon_preview(self, obj):
        """Миниатюра иконки в списке категорий"""
        if obj.icon_image:
            return format_html(
                '<img src="{}" style="width: 32px; height: 32px; border-radius: 50%; object-fit: cover;" />',
                obj.icon_image.url
            )
        elif obj.icon:
            return format_html('<span style="font-size: 1.5rem;">{}</span>', obj.icon)
        return '-'
    icon_preview.short_description = 'Иконка'

    def icon_image_preview(self, obj):
        """Превью загруженной иконки при редактировании"""
        if obj.icon_image:
            return format_html(
                '<div style="margin: 10px 0;">'
                '<p style="margin-bottom: 5px; font-weight: bold;">Текущая иконка:</p>'
                '<img src="{}" style="width: 64px; height: 64px; border-radius: 50%; object-fit: cover; border: 2px solid #ddd;" />'
                '<p style="margin-top: 5px; font-size: 0.9em; color: #666;">Размер: 32×32px (или больше для retina-дисплеев)</p>'
                '</div>',
                obj.icon_image.url
            )
        return format_html(
            '<p style="color: #999; font-style: italic;">Иконка еще не загружена. Рекомендуемый размер: 32×32px или больше</p>'
        )
    icon_image_preview.short_description = 'Превью иконки'

    def color_display(self, obj):
        return format_html(
            '<span style="background-color: {}; padding: 5px 10px; border-radius: 3px; color: white;">{}</span>',
            obj.color, obj.color
        )
    color_display.short_description = 'Цвет'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'article_count', 'created_at']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['name']


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'status', 'featured', 'pin_status_display',
                    'views_count', 'likes_count', 'comments_count', 'published_at']
    list_filter = ['status', 'category', 'featured', 'is_pinned', 'created_at', 'published_at']
    list_editable = ['status', 'featured']
    search_fields = ['title', 'content', 'excerpt', 'author__username']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['tags']
    readonly_fields = ['views_count', 'likes_count', 'comments_count', 'created_at', 'updated_at', 'reading_time_display']
    date_hierarchy = 'published_at'

    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'slug', 'subtitle', 'author', 'category', 'tags')
        }),
        ('Содержание', {
            'fields': ('content', 'excerpt')
        }),
        ('Обложка', {
            'fields': ('cover_image', 'cover_alt'),
            'classes': ('collapse',)
        }),
        ('Статус и даты', {
            'fields': ('status', 'published_at', 'created_at', 'updated_at')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
        ('Настройки', {
            'fields': ('featured', 'is_pinned', 'pin_order', 'allow_comments'),
            'description': 'Для закрепления статьи: поставьте галочку "Закреплено" и укажите порядок (1 - вверху, 2 - второй и т.д.)'
        }),
        ('Статистика', {
            'fields': ('views_count', 'likes_count', 'comments_count', 'reading_time_display'),
            'classes': ('collapse',)
        }),
    )

    def pin_status_display(self, obj):
        """Отображение статуса закрепления"""
        if obj.is_pinned and obj.pin_order > 0:
            return format_html(
                '<span style="background-color: #3B82F6; color: white; padding: 3px 8px; border-radius: 3px; font-weight: bold;">📌 {}</span>',
                obj.pin_order
            )
        elif obj.is_pinned:
            return format_html('<span style="color: #999;">📌 Без порядка</span>')
        return '-'
    pin_status_display.short_description = 'Закреплено'

    def reading_time_display(self, obj):
        return f"{obj.reading_time()} мин"
    reading_time_display.short_description = 'Время чтения'

    def save_model(self, request, obj, form, change):
        if not change:  # Если создается новая статья
            obj.author = request.user
        super().save_model(request, obj, form, change)


@admin.register(ArticleView)
class ArticleViewAdmin(admin.ModelAdmin):
    list_display = ['article', 'user', 'ip_address', 'viewed_at']
    list_filter = ['viewed_at']
    search_fields = ['article__title', 'user__username', 'ip_address']
    date_hierarchy = 'viewed_at'
    readonly_fields = ['article', 'user', 'ip_address', 'user_agent', 'viewed_at']

    def has_add_permission(self, request):
        return False


@admin.register(Reaction)
class ReactionAdmin(admin.ModelAdmin):
    list_display = ['article', 'user', 'reaction_type', 'created_at']
    list_filter = ['reaction_type', 'created_at']
    search_fields = ['article__title', 'user__username']
    date_hierarchy = 'created_at'
    readonly_fields = ['article', 'user', 'reaction_type', 'created_at']

    def has_add_permission(self, request):
        return False


# Customize Admin Site
admin.site.site_header = 'ArticleHub Admin'
admin.site.site_title = 'ArticleHub'
admin.site.index_title = 'Управление сайтом'
