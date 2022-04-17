from django import template
from portal.models import Post, Tag
from django.db.models import Count, F

register = template.Library()

@register.inclusion_tag('portal/popular_posts_tpl.html')
def get_popular_posts(cnt=5):       # значение cnt (количество постов по умолчанию) может быть переопределно в шаблоне {% get_popular_posts 3 %}
    posts = Post.objects.order_by('-views')[:cnt]
    return {"popular_posts": posts}

@register.inclusion_tag('portal/last_posts_tpl.html')
def get_last_posts(cnt=5):       # значение cnt (количество постов по умолчанию) может быть переопределно в шаблоне {% get_popular_posts 3 %}
    posts = Post.objects.order_by('-created_at')[:cnt]
    return {"last_posts": posts}

@register.inclusion_tag('portal/tags_tpl.html')
def get_tags(cnt=10):
    tags = Tag.objects.all()[:cnt]
    return {"tags": tags}

@register.inclusion_tag('portal/search_tpl.html')
def get_search_posts(cnt=10):       # значение cnt (количество постов по умолчанию) может быть переопределно в шаблоне {% get_popular_posts 3 %}
    posts = Post.objects.order_by('-created_at')[:cnt]
    return {"search_posts": posts}