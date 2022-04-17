from django.urls import path  # функция path связывает контроллер views и template (странитцами) - это функция для обработки пути
from django.views.decorators.cache import cache_page
from .views import *          # импорт из каталога контроллеров всех функций

urlpatterns = [
    path('', index, name='index'),
    #path('rubrics/', show_rubric, name='rubricss'),
    path('rubric/<str:slug>/',  PageByRubric.as_view(), name='rubric'), # список страниц выбранной категории
    path('page/<str:slug>/', GetPage.as_view(), name='page'),  # выводит полную страницу
    path('rubric/<str:slug>/', get_rubric, name='rubric'),
]
