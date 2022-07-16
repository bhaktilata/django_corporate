from django.urls import path  # функция path связывает контроллер views и template (странитцами) - это функция для обработки пути
#from django.conf.urls import include
#from django.views.decorators.cache import cache_page
#from .views import get_about
from .views import *
from django.contrib.sitemaps.views import sitemap  # виды
from blog.sitemap import PostSitemap          # Sitemap для страниц Блога
from cms.sitemap import AboutSitemap, ServiceSitemap      # Статический Sitemap для относительно постоянных страниц
from django.views.generic.base import TemplateView  # robots.txt

sitemaps = {
    'about': AboutSitemap,
    'service': ServiceSitemap,
    'dynamic': PostSitemap,
}
urlpatterns = [
    path('', Home, name='home'),
    path('page/<str:slug>/', GetPage.as_view(), name='page'), # динамические страницы об услугах и прочее
    path('about/', get_about, name='about'),
    path('service/', get_service, name='service'),
    path('feedback/', get_contact, name='contact'),
    path('rubric/', GetRubric.as_view(), name='rubric'), # список всех рубрик страниц
    path('rubric/<str:slug>/',  PageByRubric.as_view(), name='pages_list'), # список страниц выбранной рубрики
    path('page/<str:slug>/', GetPage.as_view(), name='page'), # выводит отдельную страницу
    path('portfolio/', GetPortfolio.as_view(), name='portfolio'),
    path('search/', Search.as_view(), name='search'),
    path('subscribe/', get_subscribe, name='subscribe'),
    path('sitemap.xml/', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt/', TemplateView.as_view(template_name="robots.txt", content_type="text/plain"), ),
    path('404/', get_error, name='error'),
    #path('feedback/', ContactCreate.as_view(), name='contact'),
    #path('success/', success, name='success_page'),

    #path('<str:slug>/share/', post_mailing, name='post_share'),
    #path('share/<str:slug>/', post_mailing, name='post_share'),

]
