from django.db import models
from django.contrib.auth.models import User
from articles.models import Article


class Comment(models.Model):
    """Комментарий к статье"""
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments',
                                verbose_name='Статья')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments',
                             verbose_name='Пользователь')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                               related_name='replies', verbose_name='Родительский комментарий')

    content = models.TextField('Комментарий', max_length=2000)
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)

    is_edited = models.BooleanField('Отредактирован', default=False)
    is_deleted = models.BooleanField('Удален', default=False)
    likes_count = models.PositiveIntegerField('Лайки', default=0)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['article', '-created_at']),
            models.Index(fields=['user']),
        ]

    def __str__(self):
        return f'{self.user.username} - {self.article.title[:50]}'

    def get_replies(self):
        """Получить ответы на комментарий"""
        return Comment.objects.filter(parent=self, is_deleted=False)

    def replies_count(self):
        """Количество ответов"""
        return self.get_replies().count()


class CommentLike(models.Model):
    """Лайк комментария"""
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='comment_likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_likes')
    created_at = models.DateTimeField('Создано', auto_now_add=True)

    class Meta:
        verbose_name = 'Лайк комментария'
        verbose_name_plural = 'Лайки комментариев'
        unique_together = ['comment', 'user']
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username} - {self.comment.id}'
