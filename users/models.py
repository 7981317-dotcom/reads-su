from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    """Расширенный профиль пользователя"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile',
                                verbose_name='Пользователь')

    # Информация о пользователе
    bio = models.TextField('О себе', max_length=500, blank=True)
    avatar = models.ImageField('Аватар', upload_to='avatars/%Y/%m/', blank=True, null=True)
    cover_image = models.ImageField('Обложка профиля', upload_to='covers/users/%Y/%m/',
                                    blank=True, null=True)

    # Социальные сети
    website = models.URLField('Веб-сайт', max_length=200, blank=True)
    twitter = models.CharField('Twitter', max_length=100, blank=True)
    github = models.CharField('GitHub', max_length=100, blank=True)
    linkedin = models.CharField('LinkedIn', max_length=100, blank=True)
    telegram = models.CharField('Telegram', max_length=100, blank=True)

    # Настройки
    email_notifications = models.BooleanField('Email уведомления', default=True)
    show_email = models.BooleanField('Показывать email', default=False)
    theme = models.CharField('Тема', max_length=10, choices=[
        ('light', 'Светлая'),
        ('dark', 'Тёмная'),
        ('auto', 'Авто')
    ], default='auto')

    # Статистика
    followers_count = models.PositiveIntegerField('Подписчики', default=0)
    following_count = models.PositiveIntegerField('Подписки', default=0)

    # Даты
    created_at = models.DateTimeField('Дата регистрации', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'
        ordering = ['-created_at']

    def __str__(self):
        return f'Профиль {self.user.username}'

    def get_full_name(self):
        """Получить полное имя или username"""
        return self.user.get_full_name() or self.user.username

    def articles_count(self):
        """Количество опубликованных статей"""
        return self.user.articles.filter(status='published').count()

    def get_avatar_url(self):
        """Получить URL аватара или дефолтный"""
        if self.avatar:
            return self.avatar.url
        return '/static/images/default-avatar.png'


class Follow(models.Model):
    """Подписка на пользователя"""
    follower = models.ForeignKey(User, on_delete=models.CASCADE,
                                 related_name='following', verbose_name='Подписчик')
    following = models.ForeignKey(User, on_delete=models.CASCADE,
                                  related_name='followers', verbose_name='На кого подписан')
    created_at = models.DateTimeField('Дата подписки', auto_now_add=True)

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        unique_together = ['follower', 'following']
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['follower', '-created_at']),
            models.Index(fields=['following', '-created_at']),
        ]

    def __str__(self):
        return f'{self.follower.username} подписан на {self.following.username}'


# Сигнал для автоматического создания профиля при регистрации пользователя
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Создание профиля при создании пользователя"""
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Сохранение профиля при сохранении пользователя"""
    if hasattr(instance, 'profile'):
        instance.profile.save()
