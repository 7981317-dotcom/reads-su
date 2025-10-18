from django import forms
from .models import Article, Category, Tag


class ArticleForm(forms.ModelForm):
    """Форма для создания и редактирования статьи"""

    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label='Теги'
    )

    class Meta:
        model = Article
        fields = [
            'title',
            'slug',
            'subtitle',
            'content',
            'excerpt',
            'category',
            'tags',
            'cover_image',
            'cover_video',
            'cover_video_url',
            'cover_alt',
            'status',
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Введите заголовок статьи...',
                'maxlength': '250'
            }),
            'slug': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'URL статьи (латиница, цифры, дефисы)',
                'maxlength': '250',
                'pattern': '[a-z0-9-]+',
            }),
            'subtitle': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Подзаголовок (необязательно)',
                'maxlength': '300'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Напишите вашу статью здесь... Поддерживается Markdown',
                'rows': 20,
                'id': 'editor-content'
            }),
            'excerpt': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Краткое описание (необязательно, генерируется автоматически)',
                'rows': 3,
                'maxlength': '500'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select',
            }),
            'cover_image': forms.FileInput(attrs={
                'class': 'form-file',
                'accept': 'image/*',
                'id': 'cover-image-upload'
            }),
            'cover_video': forms.FileInput(attrs={
                'class': 'form-file',
                'accept': 'video/mp4,video/webm,video/ogg',
                'id': 'cover-video-upload'
            }),
            'cover_alt': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Описание обложки для SEO',
                'maxlength': '200'
            }),
            'status': forms.Select(attrs={
                'class': 'form-select',
            }),
        }
        labels = {
            'title': 'Заголовок',
            'slug': 'URL',
            'subtitle': 'Подзаголовок',
            'content': 'Содержание',
            'excerpt': 'Краткое описание',
            'category': 'Категория',
            'tags': 'Теги',
            'cover_image': 'Обложка (изображение)',
            'cover_video': 'Обложка (видео)',
            'cover_alt': 'Описание обложки',
            'status': 'Статус',
        }
        help_texts = {
            'slug': 'Оставьте пустым для автоматической генерации из заголовка. Только латинские буквы, цифры и дефисы',
            'content': 'Используйте Markdown для форматирования текста. Можете вставлять изображения и видео',
            'excerpt': 'Если не указано, будет сгенерировано автоматически',
            'cover_image': 'Изображение обложки (JPG, PNG, WebP)',
            'cover_video': 'Видео обложка (MP4, WebM). Если загружено, будет использоваться вместо изображения',
            'cover_alt': 'Альтернативный текст для обложки (для SEO и доступности)',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Добавляем пустой вариант для категории
        self.fields['category'].empty_label = '-- Выберите категорию --'
        self.fields['category'].required = True
        # Делаем slug необязательным (генерируется автоматически)
        self.fields['slug'].required = False
