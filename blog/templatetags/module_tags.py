from django import template
from blog.models import Post, Tag
from django.db.models import Count, F

register = template.Library()

@register.inclusion_tag('blog/popular_posts_tpl.html')
def get_popular(cnt=3):       # значение cnt (количество постов по умолчанию) может быть переопределно в шаблоне {% get_popular_posts 3 %}
    posts = Post.objects.filter(visible=True).order_by('-views')[:cnt]
    return {"popular_posts": posts}

@register.inclusion_tag('blog/last_posts_tpl.html')
def get_last(cnt=3):       # значение cnt (количество постов по умолчанию) может быть переопределно в шаблоне {% get_popular_posts 3 %}
    posts = Post.objects.filter(visible=True).order_by('-created_at')[:cnt]
    return {"last_posts": posts}

@register.inclusion_tag('blog/tags_tpl.html')
def get_tags(cnt=10):
    tags = Tag.objects.all()[:cnt]
    return {"tags": tags}

@register.inclusion_tag('blog/search_tpl.html')
def get_search_posts(cnt=10):       # значение cnt (количество постов по умолчанию) может быть переопределно в шаблоне {% get_popular_posts 3 %}
    posts = Post.objects.order_by('-created_at')[:cnt]
    return {"search_posts": posts}