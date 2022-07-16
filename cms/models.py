from django.db import models
from django.urls import reverse

class Tag(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, verbose_name='Псевдоним', unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('tag', kwargs={"slug": self.slug})  # маршрут/словарь

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'
        ordering = ['title']

class Rubric(models.Model):
    title = models.CharField(max_length=255, db_index=True, verbose_name='Название')
    title_menu = models.CharField(max_length=255, verbose_name='Название в меню')
    slug = models.SlugField(max_length=255, verbose_name='Псевдоним', unique=True)
    description = models.TextField(blank=True, verbose_name='Описание')
    content = models.TextField(blank=True, verbose_name='Контент')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True, verbose_name='Изображение!!')
    visible = models.BooleanField(default=True, verbose_name='Видимость')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('rubric', kwargs={"slug": self.slug})  # маршрут/словарь - функция reverse работает в пайтон файлах
                                                             # тогда как функция url {% url 'category' item.slug %} в шаблонах
    class Meta:
        verbose_name = 'Рубрика(ю)'
        verbose_name_plural = 'Рубрики'
        ordering = ['title']

class Page(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    title_seo = models.CharField(blank=True, max_length=255, verbose_name='Заголовок для меню')
    slug = models.SlugField(max_length=255, verbose_name='Псевдоним', unique=True)
    rubric = models.ForeignKey(Rubric, related_name="pages_rubric", on_delete=models.SET_NULL, null=True, verbose_name='Рубрика')
    description = models.CharField(max_length=255, blank=True, verbose_name='Описание')
    intro_text = models.TextField(blank=True, verbose_name='Аннотация')
    full_text = models.TextField(blank=True, verbose_name='Контент')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True, verbose_name='Изображение')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Опубликовано')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')
    views = models.IntegerField(default=0, verbose_name='Хиты')
    visible = models.BooleanField(default=True, verbose_name='Видимость')
    feature = models.BooleanField(default=False, verbose_name='Рекомендуем')

    def __str__(self): # магический метод, возвращает строкоеое представление объекькта object
        return self.title

    def get_absolute_url(self):
        return reverse('page', kwargs={"slug": self.slug})  # маршрут/словарь

    class Meta:
        verbose_name = 'Страница(у)'
        verbose_name_plural = 'Страницы'
        ordering = ['-created_at']

class Service(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    slug = models.SlugField(max_length=255, verbose_name='Псевдоним', unique=True)
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
        return reverse('service', kwargs={"slug": self.slug})  # маршрут/словарь

    class Meta:
        verbose_name = 'Услуга(у)'
        verbose_name_plural = 'Услуги'
        ordering = ['-title']

class Portfolio(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    slug = models.SlugField(max_length=255, verbose_name='Псевдоним', unique=True)
    description = models.CharField(max_length=255, blank=True, verbose_name='Описание')
    intro_text = models.TextField(blank=True, verbose_name='Аннотация')
    full_text = models.TextField(blank=True, verbose_name='Контент')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True, verbose_name='Изображение')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Опубликовано')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')
    is_published = models.BooleanField(default=True, verbose_name='Опубликован?')
    views = models.IntegerField(default=0, verbose_name='Хиты')
    visible = models.BooleanField(default=True, verbose_name='Видимость')

    def __str__(self):  # магический метод, возвращает строкоеое представление объекькта object
        return self.title

    def get_absolute_url(self):
        return reverse('service', kwargs={"slug": self.slug})  # маршрут/словарь

    class Meta:
        verbose_name = 'Услуга(у)'
        verbose_name_plural = 'Услуги'
        ordering = ['-title']

class Contact(models.Model):
    first_name = models.CharField(max_length=200, verbose_name='Имя пользователя')
    last_name = models.CharField(max_length=200, verbose_name='Фамилия пользователя')
    email = models.EmailField(max_length=200, verbose_name='Почта пользователя')
    subject = models.CharField(max_length=200, verbose_name='Тема сообщения')
    message = models.TextField(max_length=1000, verbose_name='Сообщение')

    def __str__(self):
        # Будет отображаться следующее поле в панели администрирования
        return self.email

    class Meta:
        verbose_name = 'Контакты'
        verbose_name_plural = 'Контакты'
        ordering = ['first_name']