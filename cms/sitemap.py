from django.contrib.sitemaps import Sitemap
from .models import Page
from django.shortcuts import reverse

class PageSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return Page.objects.all().filter(visible=True)
    def lastmod(self, obj):
        return obj.updated_at

class AboutSitemap(Sitemap):

    def items(self):
        return ['about']
    def location(self, item):
        return reverse(item)

class ServiceSitemap(Sitemap):

    def items(self):
        return ['service']
    def location(self, item):
        return reverse(item)