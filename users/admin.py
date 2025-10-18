from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile, Follow


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Профиль'
    fk_name = 'user'
    fields = ['avatar', 'bio', 'website', 'twitter', 'github', 'linkedin', 'telegram',
              'email_notifications', 'show_email', 'theme']


class CustomUserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'date_joined']
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'date_joined']


# Перерегистрация User с новым админом
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'articles_count', 'followers_count', 'following_count', 'created_at']
    search_fields = ['user__username', 'user__email', 'bio']
    list_filter = ['theme', 'created_at']
    readonly_fields = ['followers_count', 'following_count', 'created_at', 'updated_at']

    fieldsets = (
        ('Пользователь', {
            'fields': ('user',)
        }),
        ('Информация', {
            'fields': ('avatar', 'cover_image', 'bio')
        }),
        ('Социальные сети', {
            'fields': ('website', 'twitter', 'github', 'linkedin', 'telegram')
        }),
        ('Настройки', {
            'fields': ('email_notifications', 'show_email', 'theme')
        }),
        ('Статистика', {
            'fields': ('followers_count', 'following_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ['follower', 'following', 'created_at']
    search_fields = ['follower__username', 'following__username']
    list_filter = ['created_at']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at']
