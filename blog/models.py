from django.db import models
from users.models import User
from mptt.models import MPTTModel, TreeForeignKey
from django.urls import reverse

class Category(MPTTModel):
    title = models.CharField(max_length=255, db_index=True, verbose_name='Название')
    title_menu = models.CharField(max_length=255, verbose_name='Название в меню')
    slug = models.SlugField(max_length=255, verbose_name='Псевдоним', unique=True)
    description = models.TextField(blank=True, verbose_name='Описание')
    content = models.TextField(blank=True, verbose_name='Контент')
    #parent_id = models.IntegerField(default=0, verbose_name='Родительская категория')
    parent = TreeForeignKey('self', models.SET_NULL, null=True, blank=True, related_name='children', verbose_name='Родитель', ) # поле необязательно - null=True, может быть пустое - blank=True
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True, verbose_name='Изображение!!')
    visible = models.BooleanField(default=True, verbose_name='Видимость')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category', kwargs={"slug": self.slug})  # маршрут/словарь - функция reverse работает в пайтон файлах
                                                             # тогда как функция url {% url 'category' item.slug %} в шаблонах
    class MPTTMeta:
        verbose_name = 'Категория(ю)'
        verbose_name_plural = 'Категории'
        order_insertion_by = ['title']


class Tag(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, verbose_name='Псевдоним', unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('tag', kwargs={"slug": self.slug})  # маршрут/словарь

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'
        ordering = ['title']

class Author(models.Model):
    name = models.CharField(max_length=150, verbose_name='Имя')
    surname = models.CharField(max_length=150, verbose_name='Фамилия')
    username = models.SlugField(max_length=255, verbose_name='Псевдоним', unique=True)
    avatara = models.ImageField(upload_to='avataras/%Y/%m/%d/', blank=True, verbose_name='Аватара')
    email_address = models.EmailField(max_length=100)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('author', kwargs={"username": self.username})  # маршрут/словарь

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'
        ordering = ['username']

class Post(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    title_seo = models.CharField(blank=True, max_length=255, verbose_name='Заголовок для меню')
    slug = models.SlugField(max_length=255, verbose_name='Псевдоним', unique=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='posts_user', blank=True, verbose_name='Автор статьи')
    category = models.ForeignKey(Category, related_name="posts_category", on_delete=models.SET_NULL, null=True, verbose_name='Категория')
    description = models.CharField(max_length=255, blank=True, verbose_name='Описание')
    intro_text = models.TextField(blank=True, verbose_name='Аннотация')
    full_text = models.TextField(blank=True, verbose_name='Контент')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True, verbose_name='Изображение')
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts')
    likes = models.IntegerField(default=0, verbose_name='Лайки')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')
    views = models.IntegerField(default=0, verbose_name='Хиты')
    visible = models.BooleanField(default=True, verbose_name='Видимость')
    feature = models.BooleanField(default=False, verbose_name='Слайдер')

    #def __str__(self): # магический метод, возвращает строкоеое представление объекькта object
    #    return self.title

    def get_absolute_url(self):
        #return reverse('post_single', kwargs={"slug": self.slug})
        return reverse('post_single', kwargs={"slug": self.category.slug, "slug": self.slug})  # маршрут в urls.py/словарь

    def get_comments(self):
        return self.comment.all()

    class Meta:
        verbose_name = 'Статья(ю)'
        verbose_name_plural = 'Статьи'
        ordering = ['-created_at']

class Comment(models.Model):
    #name = models.CharField(max_length=100, verbose_name='Автор комментария')
    name = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments_user', blank=True, null = True, verbose_name='Автор комментария')
    email = models.EmailField(max_length=100, verbose_name='Адрес')
    website = models.CharField(max_length=150, verbose_name='Web-сайт')
    message = models.TextField(max_length=500, verbose_name='Текст комментария')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated = models.DateTimeField(auto_now=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True, related_name='comment_post', verbose_name='Статья')
    active = models.BooleanField(default=False, verbose_name='Опубликовано?')

    def get_comments(self):
        return self.comment.all()

    def get_absolute_url(self):
        return reverse('post_single', kwargs={"slug": self.slug})  # маршрут/словарь

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['created_at',]

    def __str__(self):
        return f'Комментарий {self.name} на {self.post}'