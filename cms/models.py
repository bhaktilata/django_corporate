from django.db import models
from django.urls import reverse
from portal.models import Author
from .models import *

class Rubric(models.Model):
    title = models.CharField(max_length=255, db_index=True, verbose_name='Название')
    title_menu = models.CharField(max_length=255, verbose_name='Название в меню')
    slug = models.SlugField(max_length=255, verbose_name='Псевдоним', unique=True)
    description = models.TextField(blank=True, verbose_name='Описание')
    content = models.TextField(blank=True, verbose_name='Контент')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True, verbose_name='Изображение!!')
    visible = models.IntegerField(default=1, verbose_name='Видимость')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('rubric', kwargs={"slug": self.slug})  # маршрут/словарь - функция reverse работает в пайтон файлах
                                                             # тогда как функция url {% url 'category' item.slug %} в шаблонах
    class Meta:
        verbose_name = 'Категория(ю)'
        verbose_name_plural = 'Категории'
        ordering = ['title']


class Page(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    title_seo = models.CharField(blank=True, max_length=255, verbose_name='Заголовок для меню')
    slug = models.SlugField(max_length=255, verbose_name='Псевдоним', unique=True)
    author = models.ForeignKey(Author, on_delete=models.PROTECT, related_name='page', blank=True, verbose_name='Автор')
    rubric = models.ForeignKey(Rubric, on_delete=models.CASCADE, verbose_name='Категория')
    description = models.CharField(max_length=255, blank=True, verbose_name='Описание')
    intro_text = models.TextField(blank=True, verbose_name='Аннотация')
    full_text = models.TextField(blank=True, verbose_name='Контент')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True, verbose_name='Изображение')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Опубликовано')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')
    views = models.IntegerField(default=0, verbose_name='Хиты')
    visible = models.BooleanField(default=True, verbose_name='Видимость')

    def __str__(self): # магический метод, возвращает строкоеое представление объекькта object
        return self.title

    def get_absolute_url(self):
        return reverse('page', kwargs={"slug": self.slug})  # маршрут/словарь

    class Meta:
        verbose_name = 'Страница(у)'
        verbose_name_plural = 'Страницы'
        ordering = ['-created_at']
