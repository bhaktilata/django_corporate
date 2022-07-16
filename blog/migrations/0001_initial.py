# Generated by Django 4.0.4 on 2022-05-28 14:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Имя')),
                ('surname', models.CharField(max_length=150, verbose_name='Фамилия')),
                ('username', models.SlugField(max_length=255, unique=True, verbose_name='Псевдоним')),
                ('avatara', models.ImageField(blank=True, upload_to='avataras/%Y/%m/%d/', verbose_name='Аватара')),
                ('email_address', models.EmailField(max_length=100)),
            ],
            options={
                'verbose_name': 'Автор',
                'verbose_name_plural': 'Авторы',
                'ordering': ['username'],
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=255, verbose_name='Название')),
                ('title_menu', models.CharField(max_length=255, verbose_name='Название в меню')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='Псевдоним')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
                ('content', models.TextField(blank=True, verbose_name='Контент')),
                ('photo', models.ImageField(blank=True, upload_to='photos/%Y/%m/%d/', verbose_name='Изображение!!')),
                ('visible', models.BooleanField(default=True, verbose_name='Видимость')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=100, verbose_name='Адрес')),
                ('website', models.CharField(max_length=150, verbose_name='Web-сайт')),
                ('message', models.TextField(max_length=500, verbose_name='Текст комментария')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создан')),
                ('updated', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=False, verbose_name='Опубликовано?')),
            ],
            options={
                'verbose_name': 'Комментарий',
                'verbose_name_plural': 'Комментарии',
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('slug', models.SlugField(max_length=100, unique=True, verbose_name='Псевдоним')),
            ],
            options={
                'verbose_name': 'Тэг',
                'verbose_name_plural': 'Тэги',
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Заголовок')),
                ('title_seo', models.CharField(blank=True, max_length=255, verbose_name='Заголовок для меню')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='Псевдоним')),
                ('description', models.CharField(blank=True, max_length=255, verbose_name='Описание')),
                ('intro_text', models.TextField(blank=True, verbose_name='Аннотация')),
                ('full_text', models.TextField(blank=True, verbose_name='Контент')),
                ('photo', models.ImageField(blank=True, upload_to='photos/%Y/%m/%d/', verbose_name='Изображение')),
                ('likes', models.IntegerField(default=0, verbose_name='Лайки')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Опубликовано')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Обновлено')),
                ('views', models.IntegerField(default=0, verbose_name='Хиты')),
                ('visible', models.BooleanField(default=True, verbose_name='Видимость')),
                ('feature', models.BooleanField(default=False, verbose_name='Слайдер')),
                ('author', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='posts_user', to='blog.author', verbose_name='Автор статьи')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='posts_category', to='blog.category', verbose_name='Категория')),
                ('tags', models.ManyToManyField(blank=True, related_name='posts', to='blog.tag')),
            ],
            options={
                'verbose_name': 'Статья(ю)',
                'verbose_name_plural': 'Статьи',
                'ordering': ['-created_at'],
            },
        ),
    ]