from django.shortcuts import render, get_object_or_404, redirect
from users.forms import UserLoginForm, UserRegisterForm, UserProfileForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import auth, messages
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from users.forms import AuthUserForm, UserRegisterForm


def user_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST) # создаем экземпляр формы и заполняем данными из POST (формы), затем передаем в контекст
        if form.is_valid():
            user = form.save()        # если форма валидна, то объект пользователя сохраеняем в переменной user
            login(request, user)      # и сразу вызываем метод login, передав ему request  и полученного прользовател для его авторизации, поэтому пользователю не придется авторизоваться
            messages.success(request, 'Вы успешно зарегистрировались') # используем компонет джанго messages об успехе, выводится в base.html перед контентом
            return redirect('home')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = UserRegisterForm()      # иначе показываем не связанную с данными форму (пустая)
    return render(request, 'users/register.html', {"form": form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST) # создаем экземпляр формы UserLoginForm
        if form.is_valid():
            user = form.get_user()   # получаем пользователя из формы
            login(request, user)      # передаем user в метод login
            return redirect('home')
    else:
        form = UserLoginForm()  # создвем обхъект класса и эта  форма передается в шаблон для отображения
    return render(request, 'users/login.html', {"form": form})

def user_logout(request):
    auth.logout(request)  # работает и так logout(request)
    return redirect('login')

def get_profile(request):
    user = request.user
    if request.method == 'POST':
        form = UserProfileForm(data = request.POST, files=request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=user)
    context = {
        'form': form, 'title': 'Личный кабинет',
    }  # baskets импортируем из модели Products
    return render(request, 'users/profile.html', context)



def get_error(request):
    return render(request, 'users/404.html')


