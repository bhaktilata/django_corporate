from django.contrib.sitemaps import Sitemap
from blog.models import Post
from django.shortcuts import reverse


class PostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Post.published.all()

    def lastmod(self, obj):
        return obj.updated

    def location(self, item):
        # return reverse('news-page', args=[item.pk])
        return f'/post/{item.pk}/'