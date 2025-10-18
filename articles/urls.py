from django.urls import path, re_path
from . import views

app_name = 'articles'

urlpatterns = [
    # Главная страница
    path('', views.home, name='home'),

    # Категории
    path('categories/', views.category_list, name='categories'),
    re_path(r'^category/(?P<slug>[-\w]+)/$', views.category_detail, name='category'),

    # Теги (поддержка unicode для кириллицы)
    re_path(r'^tag/(?P<slug>[-\w]+)/$', views.tag_detail, name='tag'),

    # Статьи
    path('create/', views.article_create, name='create'),
    path('my-articles/', views.my_articles, name='my_articles'),
    re_path(r'^article/(?P<slug>[-\w]+)/$', views.article_detail, name='detail'),
    re_path(r'^article/(?P<slug>[-\w]+)/edit/$', views.article_edit, name='edit'),
    re_path(r'^article/(?P<slug>[-\w]+)/delete/$', views.article_delete, name='delete'),

    # Реакции (AJAX)
    re_path(r'^article/(?P<slug>[-\w]+)/reaction/$', views.toggle_reaction, name='toggle_reaction'),

    # Загрузка медиа (AJAX)
    path('upload-media/', views.upload_media, name='upload_media'),

    # Поиск
    path('search/', views.search, name='search'),

    # SEO и статические страницы
    path('robots.txt', views.robots_txt, name='robots'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('privacy/', views.privacy, name='privacy'),
    path('terms/', views.terms, name='terms'),
]
