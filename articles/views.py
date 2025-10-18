from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.http import JsonResponse
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os
from .models import Article, Category, Tag, Reaction
from comments.models import Comment
from .forms import ArticleForm


def home(request):
    """Главная страница со списком статей"""
    articles_list = Article.objects.filter(status='published').select_related(
        'author', 'category'
    ).prefetch_related('tags').order_by('-is_pinned', 'pin_order', '-published_at')

    # Фильтры
    category_slug = request.GET.get('category')
    tag_slug = request.GET.get('tag')
    search_query = request.GET.get('q')

    if category_slug:
        articles_list = articles_list.filter(category__slug=category_slug)

    if tag_slug:
        articles_list = articles_list.filter(tags__slug=tag_slug)

    if search_query:
        articles_list = articles_list.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query) |
            Q(excerpt__icontains=search_query)
        )

    # Пагинация
    paginator = Paginator(articles_list, settings.ARTICLES_PER_PAGE)
    page = request.GET.get('page')
    articles = paginator.get_page(page)

    # Популярные статьи
    popular_articles = Article.objects.filter(
        status='published'
    ).order_by('-views_count')[:5]

    # Категории с количеством статей (сортированные по количеству статей)
    categories = Category.objects.annotate(
        article_count=Count('articles', filter=Q(articles__status='published'))
    ).filter(article_count__gt=0).order_by('-article_count')

    # Популярные теги
    popular_tags = Tag.objects.annotate(
        article_count=Count('articles', filter=Q(articles__status='published'))
    ).filter(article_count__gt=0).order_by('-article_count')[:20]

    # Топ блогеры (пользователи с наибольшим количеством статей)
    top_bloggers = User.objects.annotate(
        article_count=Count('articles', filter=Q(articles__status='published'))
    ).filter(article_count__gt=0).order_by('-article_count')[:5]

    # Популярные комментарии
    popular_comments = Comment.objects.filter(
        is_deleted=False
    ).select_related('user', 'user__profile', 'article').order_by('-likes_count')[:5]

    # Общее количество статей
    total_articles = Article.objects.filter(status='published').count()

    # Текущая категория (если есть)
    current_category = None
    if category_slug:
        current_category = Category.objects.filter(slug=category_slug).first()

    context = {
        'articles': articles,
        'popular_articles': popular_articles,
        'categories': categories,
        'popular_tags': popular_tags,
        'top_bloggers': top_bloggers,
        'popular_comments': popular_comments,
        'total_articles': total_articles,
        'search_query': search_query,
        'current_category': current_category,
        'current_tag': tag_slug,
    }

    return render(request, 'articles/home.html', context)


def article_detail(request, slug):
    """Детальная страница статьи"""
    article = get_object_or_404(
        Article.objects.select_related('author', 'category').prefetch_related('tags'),
        slug=slug,
        status='published'
    )

    # Увеличить счетчик просмотров
    article.increment_views()

    # Комментарии
    comments = article.comments.filter(
        parent=None, is_deleted=False
    ).select_related('user').order_by('-created_at')

    # Похожие статьи
    related_articles = Article.objects.filter(
        category=article.category,
        status='published'
    ).exclude(id=article.id).order_by('-published_at')[:3]

    # Проверка реакций текущего пользователя
    user_reactions = {}
    if request.user.is_authenticated:
        reactions = Reaction.objects.filter(article=article, user=request.user)
        user_reactions = {r.reaction_type: True for r in reactions}

    # Популярные статьи для сайдбара
    popular_articles = Article.objects.filter(
        status='published'
    ).order_by('-views_count')[:5]

    # Категории с количеством статей (сортированные по количеству статей)
    categories = Category.objects.annotate(
        article_count=Count('articles', filter=Q(articles__status='published'))
    ).filter(article_count__gt=0).order_by('-article_count')

    # Топ блогеры
    top_bloggers = User.objects.annotate(
        article_count=Count('articles', filter=Q(articles__status='published'))
    ).filter(article_count__gt=0).order_by('-article_count')[:5]

    # Популярные комментарии
    popular_comments = Comment.objects.filter(
        is_deleted=False
    ).select_related('user', 'user__profile', 'article').order_by('-likes_count')[:5]

    # Общее количество статей
    total_articles = Article.objects.filter(status='published').count()

    context = {
        'article': article,
        'comments': comments,
        'related_articles': related_articles,
        'user_reactions': user_reactions,
        'popular_articles': popular_articles,
        'categories': categories,
        'top_bloggers': top_bloggers,
        'popular_comments': popular_comments,
        'total_articles': total_articles,
    }

    return render(request, 'articles/detail.html', context)


def category_list(request):
    """Список всех категорий"""
    categories = Category.objects.annotate(
        article_count=Count('articles', filter=Q(articles__status='published'))
    ).order_by('order', 'name')

    context = {
        'categories': categories,
    }

    return render(request, 'articles/categories.html', context)


def category_detail(request, slug):
    """Статьи по категории"""
    category = get_object_or_404(Category, slug=slug)

    articles_list = Article.objects.filter(
        category=category,
        status='published'
    ).select_related('author', 'category').prefetch_related('tags').order_by('-is_pinned', 'pin_order', '-published_at')

    paginator = Paginator(articles_list, settings.ARTICLES_PER_PAGE)
    page = request.GET.get('page')
    articles = paginator.get_page(page)

    # Популярные статьи для левого сайдбара
    popular_articles = Article.objects.filter(
        status='published'
    ).order_by('-views_count')[:5]

    # Категории с количеством статей (сортированные по количеству статей)
    categories = Category.objects.annotate(
        article_count=Count('articles', filter=Q(articles__status='published'))
    ).filter(article_count__gt=0).order_by('-article_count')

    # Топ блогеры для правого сайдбара
    top_bloggers = User.objects.annotate(
        article_count=Count('articles', filter=Q(articles__status='published'))
    ).filter(article_count__gt=0).order_by('-article_count')[:5]

    # Популярные комментарии для правого сайдбара
    popular_comments = Comment.objects.filter(
        is_deleted=False
    ).select_related('user', 'user__profile', 'article').order_by('-likes_count')[:5]

    # Общее количество статей
    total_articles = Article.objects.filter(status='published').count()

    context = {
        'current_category': category,
        'articles': articles,
        'popular_articles': popular_articles,
        'categories': categories,
        'top_bloggers': top_bloggers,
        'popular_comments': popular_comments,
        'total_articles': total_articles,
    }

    return render(request, 'articles/category_detail.html', context)


def tag_detail(request, slug):
    """Статьи по тегу"""
    tag = get_object_or_404(Tag, slug=slug)

    articles_list = Article.objects.filter(
        tags=tag,
        status='published'
    ).select_related('author', 'category').order_by('-published_at')

    paginator = Paginator(articles_list, settings.ARTICLES_PER_PAGE)
    page = request.GET.get('page')
    articles = paginator.get_page(page)

    context = {
        'tag': tag,
        'articles': articles,
    }

    return render(request, 'articles/tag_detail.html', context)


@login_required
def article_create(request):
    """Создание новой статьи"""
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user

            # Получить статус из кнопки (если нажата)
            status = request.POST.get('status', 'draft')
            article.status = status

            article.save()
            form.save_m2m()  # Сохранить многие-ко-многим отношения (теги)

            if article.status == 'published':
                messages.success(request, 'Статья успешно опубликована!')
            else:
                messages.success(request, 'Статья сохранена как черновик')

            return redirect(article.get_absolute_url() if article.status == 'published' else 'articles:my_articles')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме')
    else:
        form = ArticleForm()

    context = {
        'form': form,
        'title': 'Создать статью',
    }

    return render(request, 'articles/create.html', context)


@login_required
def article_edit(request, slug):
    """Редактирование статьи"""
    article = get_object_or_404(Article, slug=slug, author=request.user)

    if request.method == 'POST':
        # Проверка чекбоксов удаления обложек ДО обработки формы
        delete_cover_image = request.POST.get('delete_cover_image')
        delete_cover_video = request.POST.get('delete_cover_video')
        delete_cover_video_url = request.POST.get('delete_cover_video_url')

        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            saved_article = form.save(commit=False)

            # Применяем удаление обложек после валидации формы
            if delete_cover_image and saved_article.cover_image:
                # Удалить файл изображения
                saved_article.cover_image.delete(save=False)
                saved_article.cover_image = None
                messages.info(request, 'Обложка (изображение) удалена')

            if delete_cover_video and saved_article.cover_video:
                # Удалить файл видео
                saved_article.cover_video.delete(save=False)
                saved_article.cover_video = None
                messages.info(request, 'Обложка (видео файл) удалена')

            if delete_cover_video_url and saved_article.cover_video_url:
                # Очистить URL видео
                saved_article.cover_video_url = ''
                messages.info(request, 'Обложка (видео URL) удалена')

            # Получить статус из кнопки (если нажата)
            status = request.POST.get('status', saved_article.status)
            saved_article.status = status

            saved_article.save()
            form.save_m2m()

            if saved_article.status == 'published':
                messages.success(request, 'Изменения успешно сохранены!')
                return redirect(saved_article.get_absolute_url())
            else:
                messages.success(request, 'Черновик сохранен')
                return redirect('articles:my_articles')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме')
    else:
        form = ArticleForm(instance=article)

    context = {
        'form': form,
        'article': article,
        'title': 'Редактировать статью',
    }

    return render(request, 'articles/create.html', context)


@login_required
def article_delete(request, slug):
    """Удаление статьи"""
    article = get_object_or_404(Article, slug=slug, author=request.user)

    if request.method == 'POST':
        article.delete()
        messages.success(request, 'Статья успешно удалена')
        return redirect('articles:my_articles')

    context = {
        'article': article,
    }

    return render(request, 'articles/delete_confirm.html', context)


@login_required
def my_articles(request):
    """Мои статьи"""
    articles_list = Article.objects.filter(
        author=request.user
    ).order_by('-created_at')

    # Фильтр по статусу
    status = request.GET.get('status')
    if status:
        articles_list = articles_list.filter(status=status)

    paginator = Paginator(articles_list, settings.ARTICLES_PER_PAGE)
    page = request.GET.get('page')
    articles = paginator.get_page(page)

    # Статистика
    stats = {
        'total': Article.objects.filter(author=request.user).count(),
        'published': Article.objects.filter(author=request.user, status='published').count(),
        'draft': Article.objects.filter(author=request.user, status='draft').count(),
        'archived': Article.objects.filter(author=request.user, status='archived').count(),
    }

    context = {
        'articles': articles,
        'stats': stats,
        'current_status': status,
    }

    return render(request, 'articles/my_articles.html', context)


@login_required
def toggle_reaction(request, slug):
    """Лайк/закладка статьи (AJAX)"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid method'})

    article = get_object_or_404(Article, slug=slug, status='published')

    import json
    data = json.loads(request.body)
    reaction_type = data.get('reaction_type', 'like')

    if reaction_type not in ['like', 'bookmark']:
        return JsonResponse({'success': False, 'error': 'Invalid reaction type'})

    # Проверить существующую реакцию
    reaction = Reaction.objects.filter(
        article=article,
        user=request.user,
        reaction_type=reaction_type
    ).first()

    if reaction:
        # Удалить реакцию
        reaction.delete()
        active = False
    else:
        # Создать реакцию
        Reaction.objects.create(
            article=article,
            user=request.user,
            reaction_type=reaction_type
        )
        active = True

    # Обновить счетчик лайков
    if reaction_type == 'like':
        count = article.reactions.filter(reaction_type='like').count()
        article.likes_count = count
        article.save(update_fields=['likes_count'])
    else:
        count = article.reactions.filter(reaction_type='bookmark').count()

    return JsonResponse({
        'success': True,
        'active': active,
        'count': count
    })


def search(request):
    """Поиск статей"""
    query = request.GET.get('q', '')

    if query:
        articles_list = Article.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(excerpt__icontains=query),
            status='published'
        ).select_related('author', 'category').order_by('-published_at')
    else:
        articles_list = Article.objects.none()

    paginator = Paginator(articles_list, settings.ARTICLES_PER_PAGE)
    page = request.GET.get('page')
    articles = paginator.get_page(page)

    context = {
        'articles': articles,
        'query': query,
        'total_results': articles_list.count(),
    }

    return render(request, 'articles/search.html', context)


@login_required
def upload_media(request):
    """API для загрузки медиа файлов (изображения и видео)"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid method'})

    if 'file' not in request.FILES:
        return JsonResponse({'success': False, 'error': 'No file uploaded'})

    uploaded_file = request.FILES['file']
    file_extension = os.path.splitext(uploaded_file.name)[1].lower()

    # Проверка типа файла
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
    video_extensions = ['.mp4', '.webm', '.ogg', '.mov']

    if file_extension in image_extensions:
        media_type = 'image'
        upload_path = f'articles/content/images/{request.user.id}/'
    elif file_extension in video_extensions:
        media_type = 'video'
        upload_path = f'articles/content/videos/{request.user.id}/'
    else:
        return JsonResponse({
            'success': False,
            'error': f'Неподдерживаемый формат файла: {file_extension}'
        })

    # Проверка размера файла (макс 50MB для видео, 5MB для изображений)
    max_size = 50 * 1024 * 1024 if media_type == 'video' else 5 * 1024 * 1024
    if uploaded_file.size > max_size:
        max_size_mb = max_size / (1024 * 1024)
        return JsonResponse({
            'success': False,
            'error': f'Файл слишком большой. Максимальный размер: {max_size_mb}MB'
        })

    # Сохранение файла
    try:
        from datetime import datetime
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{uploaded_file.name}"
        file_path = upload_path + filename

        saved_path = default_storage.save(file_path, ContentFile(uploaded_file.read()))
        file_url = default_storage.url(saved_path)

        return JsonResponse({
            'success': True,
            'url': file_url,
            'type': media_type,
            'filename': uploaded_file.name
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Ошибка при загрузке файла: {str(e)}'
        })


def robots_txt(request):
    """Отдача robots.txt"""
    from django.http import HttpResponse
    from django.views.decorators.http import require_GET

    lines = [
        "User-agent: *",
        "Allow: /",
        "Disallow: /admin/",
        "Disallow: /users/login/",
        "Disallow: /users/register/",
        "Disallow: /users/logout/",
        "Disallow: /articles/create/",
        "Disallow: /articles/*/edit/",
        "Disallow: /articles/*/delete/",
        "Disallow: /media/",
        "Disallow: /static/admin/",
        "Crawl-delay: 1",
        f"Sitemap: {request.build_absolute_uri('/sitemap.xml')}",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


def about(request):
    """Страница О нас"""
    return render(request, 'articles/about.html')


def contact(request):
    """Страница Контакты"""
    return render(request, 'articles/contact.html')


def privacy(request):
    """Страница Политика конфиденциальности"""
    return render(request, 'articles/privacy.html')


def terms(request):
    """Страница Условия использования"""
    return render(request, 'articles/terms.html')
