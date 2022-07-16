from django.urls import path  # функция path связывает контроллер views и template (странитцами) - это функция для обработки пути
from .views import *

#app_name = 'users'

urlpatterns = [
    #path('register/', UserRegisterView.as_view(), name='register'),
    path('register/', user_register, name='register'),
    #path('login/', UserLoginView.as_view(), name='login'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('404/', get_error, name='error'),
    path('profile/', get_profile, name='profile'),


 
]