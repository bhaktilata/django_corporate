from django import forms
#from snowpenguin.django.recaptcha3.fields import ReCaptchaField
from .models import Post, Comment
import re
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, \
    AuthenticationForm  # форма создания и аутентификации пользователя
from django.contrib.auth.models import User

class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label='Имя пользователя', help_text='Имя должно содержать не более 150 символов', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='E-mail', widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        # fields = '__all__'
        fields = ['title', 'slug', 'description', 'author', 'intro_text', 'full_text', 'photo', 'visible']
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
'''
class CommentForm(forms.ModelForm):
    # captcha = ReCaptchaField()

    class Meta:
        model = Comment
        fields = ('message', 'name', 'email', 'website',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        widgets = {
            'message': forms.Textarea(attrs={'class': 'form-control', 'cols': 50, 'rows': 5}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'website': forms.TextInput(attrs={'class': 'form-control'}),
        }

'''

#forms.py
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('message', 'name', 'email', 'website',)
        #fields = ('message',)
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
        self.fields['message'].widget = forms.Textarea(attrs={'rows':5})

