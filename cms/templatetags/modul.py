from django import template
from cms.models import Tag
from django.db.models import Count, F

register = template.Library()
'''
@register.inclusion_tag('cms/popular_posts_tpl.html')
def get_popular_posts(cnt=3):       # значение cnt (количество постов по умолчанию) может быть переопределно в шаблоне {% get_popular_posts 3 %}
    posts = Post.objects.order_by('-views')[:cnt]
    return {"popular_posts": posts}
'''
'''
@register.inclusion_tag('cms/last_posts_tpl.html')
def get_last_posts(cnt=2):       # значение cnt (количество постов по умолчанию) может быть переопределно в шаблоне {% get_popular_posts 3 %}
    posts = Post.objects.order_by('-created_at')[:cnt]
    return {"last_posts": posts}
'''
@register.inclusion_tag('cms/tags_tpl.html')
def get_tags(cnt=10):
    tags = Tag.objects.all()[:cnt]
    return {"tags": tags}
'''
@register.inclusion_tag('cms/search_tpl.html')
def get_search_posts(cnt=10):       # значение cnt (количество постов по умолчанию) может быть переопределно в шаблоне {% get_popular_posts 3 %}
    posts = Post.objects.order_by('-created_at')[:cnt]
    return {"search_posts": posts}
'''