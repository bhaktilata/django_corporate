from django import forms
from blog.models import Post

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm # форма создания и аутентификации пользователя
import re
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()

class UserLoginForm(AuthenticationForm):  # мы создаем эту форму для того, чтобы иметь возможность настроить ее внешний вид через виджеты и классы и класс Meta здесь не нужен
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-text'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-text'}))
'''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
'''
class AuthUserForm(AuthenticationForm, forms.ModelForm):  # логин форма
    class Meta:
        model = User
        fields = ('username','password')
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
'''
class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label='Имя пользователя', help_text='Имя должно содержать не более 150 символов', widget=forms.TextInput(attrs={'class': 'form-text'}))
    email = forms.EmailField(label='E-mail', widget=forms.EmailInput(attrs={'class': 'form-text'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-text'}))
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput(attrs={'class': 'form-text'}))

    class Meta:
        model = User                  # это не пользовательская модель, а джанговыская
        fields = ('username', 'email', 'password1', 'password2')
'''

class UserRegisterForm(forms.ModelForm):  # внешниц вид не ахти и пароль вносится только один раз, без подтверждения
    class Meta:
        model = User
        fields = ('username','password')
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user
'''
class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25) # имя отправителя письма
    email = forms.EmailField()             # почтовый адрес отправителя
    to = forms.EmailField()               # адрес кудп отправить сообщение
    comments = forms.CharField(required=False, widget=forms.Textarea) # текст сообщения
'''
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        # fields = '__all__'
        fields = ['title', 'slug', 'description', 'author', 'intro_text', 'full_text', 'photo', 'visible' ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.Select(attrs={'class': 'form-control'}),
            'intro_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'full_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if re.match(r'\d', title):
            raise ValidationError('Название не должно начинаться с цифры')
        return title

class UserProfileForm(UserChangeForm):

    username = forms.CharField(widget=forms.TextInput(attrs={'readonly': True}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'readonly': True}))
    first_name = forms.CharField(label='Имя', widget=forms.TextInput())
    last_name = forms.CharField(label='Фамилия', widget=forms.TextInput())
    image = forms.ImageField(label='Аватара', widget=forms.FileInput(), required=False)
    #phone = forms.CharField(label='Телефон', widget=forms.TextInput())
    #adress = forms.CharField(label='Адрес доставки', widget=forms.TextInput())
    #birstday = forms.CharField(label='День рождения', widget=forms.DateInput())
    # заказы, звонки, запросы
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'image']

    def __init__(self, *args, **kwarga):
        super(UserProfileForm, self).__init__(*args, **kwarga)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control py-4'
            self.fields['image'].widget.attrs['class'] = 'custom-file-input'
