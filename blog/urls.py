from django.urls import path
from .views import *


urlpatterns = [
    path('', get_blog, name='index'),
    path('category/', GetCategory.as_view(), name='categories'), # список всех категорий
    path('category/<str:slug>/', PostByCategory.as_view(), name='category'),  # список статей выбранной категории
    path('post/<str:slug>/', GetPost.as_view(), name='post_single'), # выводит полную статью
    path('tag/<str:slug>/', PostsByTag.as_view(), name='tag'), # Выводит материалы по тегу
    path('author/<str:slug>/', get_author, name='author'),
    path('404/', get_error, name='error'),
    #path('comment/<str:slug>/', CreateComment.as_view(), name="create_comment"),
    #path('<str:slug>/<str:post_slug>/', CreateComment.as_view(), name="create_comment"),
    #path('<slug:slug>/<str:post_slug>/', CreateComment.as_view(), name="create_comment"),
    #path('recipe/<str:slug>/', post_comment, name='recipe'),  # выводит полный рецепт





]

