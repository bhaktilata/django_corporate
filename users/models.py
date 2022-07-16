from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    #username = models.CharField(max_length=50, unique=True, verbose_name='Логин')
    #firstname = models.CharField(max_length=50, unique=True, verbose_name='Имя')
    #lastname = models.CharField(max_length=50, unique=True, verbose_name='Фамилия')
    #email = models.EmailField(max_length=100, unique=True, verbose_name='E-mail')
    #password = models.CharField(max_length=50)
    image = models.ImageField(upload_to='users_images', blank=True, verbose_name='Фотография')
    #phone = models.CharField(max_length=50, verbose_name='Телефон')
    #birstday = models.CharField(max_length=50, verbose_name='День рождения')
    #address = models.CharField(max_length=50, verbose_name='Адрес доставки')
    #description = models.TextField(max_length=500, verbose_name='Описание')
    #is_active = models.BooleanField(default=True, verbose_name='Статус активации')
    #is_staff = models.BooleanField(default=False, verbose_name='Статус админа')
