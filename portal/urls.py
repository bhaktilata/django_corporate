from django.urls import path  # функция path связывает контроллер views и template (странитцами) - это функция для обработки пути
from django.views.decorators.cache import cache_page
from .views import *
from django.contrib.sitemaps.views import sitemap
from portal.sitemap import PostSitemap

sitemaps = {
    'posts': PostSitemap,
}


urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('about/', get_about, name='about'),
    path('portfolio/', Portfolio.as_view(), name='portfolio'),
    path('service/', GetService.as_view(), name='service'),
    path('category/<str:slug>/',  PostByCategory.as_view(), name='category'), # список статей выбранной категории
    path('category/', GetCategory.as_view(), name='categories'), # список всех категорий
    path('post/<str:slug>/', post_comment, name='post'),  # выводит полную статью
    path('<str:slug>/share/', post_mailing, name='post_share'),
    #path('post/<str:slug>/', GetPost.as_view(), name='post'),
    path('feedback/', get_contact, name='contact'),
    path('tag/<str:slug>/', PostsByTag.as_view(), name='tag'),
    path('search/', Search.as_view(), name='search'),
    path('sitemap.xml/', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('404/', get_error, name='error'),
    #path('share/<str:slug>/', post_mailing, name='post_share'),


]



