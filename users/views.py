from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, logout as auth_logout
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .models import UserProfile, Follow
from articles.models import Article


def register(request):
    """Регистрация нового пользователя"""
    if request.method == 'POST':
        # TODO: Добавить форму регистрации
        pass

    return render(request, 'users/register.html')


def profile(request, username):
    """Профиль пользователя"""
    user = get_object_or_404(User, username=username)
    profile = user.profile

    # Статьи пользователя
    articles = Article.objects.filter(
        author=user,
        status='published'
    ).order_by('-published_at')[:10]

    # Статистика
    stats = {
        'articles_count': Article.objects.filter(author=user, status='published').count(),
        'followers_count': profile.followers_count,
        'following_count': profile.following_count,
    }

    # Проверка подписки
    is_following = False
    if request.user.is_authenticated and request.user != user:
        is_following = Follow.objects.filter(
            follower=request.user,
            following=user
        ).exists()

    context = {
        'profile_user': user,
        'profile': profile,
        'articles': articles,
        'stats': stats,
        'is_following': is_following,
    }

    return render(request, 'users/profile.html', context)


@login_required
def settings(request):
    """Настройки профиля"""
    if request.method == 'POST':
        # TODO: Добавить форму настроек
        pass

    context = {
        'profile': request.user.profile,
    }

    return render(request, 'users/settings.html', context)


def logout_view(request):
    """Выход из системы (поддерживает GET и POST)"""
    auth_logout(request)
    messages.success(request, 'Вы успешно вышли из системы')
    return redirect('articles:home')


@require_POST
def api_register(request):
    """API для регистрации нового пользователя"""
    try:
        email = request.POST.get('email', '').strip()
        username = request.POST.get('username', '').strip()
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')

        # Validation
        if not all([email, username, password1, password2]):
            return JsonResponse({'success': False, 'error': 'Все поля обязательны для заполнения'})

        if password1 != password2:
            return JsonResponse({'success': False, 'error': 'Пароли не совпадают'})

        if len(password1) < 6:
            return JsonResponse({'success': False, 'error': 'Пароль должен быть не менее 6 символов'})

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            return JsonResponse({'success': False, 'error': 'Пользователь с таким email уже существует'})

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            return JsonResponse({'success': False, 'error': 'Пользователь с таким именем уже существует'})

        # Create user (using email as username for login)
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )

        # Login user immediately after registration
        login(request, user)

        return JsonResponse({'success': True})

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
