from django import forms
from .models import Page, Rubric, Contact
import re
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.forms import Textarea

class EmailPostForm(forms.Form): # отправка сообщения со страницы поста
    name = forms.CharField(max_length=25) # имя отправителя письма
    email = forms.EmailField()             # почтовый адрес отправителя
    to = forms.EmailField()               # адрес кудп отправить сообщение
    comments = forms.CharField(required=False, widget=forms.Textarea) # текст сообщения
'''
class ContactForm(forms.Form):
    name = forms.CharField(label='Имя', max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='E-mail', max_length=150, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    subject = forms.CharField(label='Тема', widget=forms.TextInput(attrs={'class': 'form-control'}))
    message = forms.CharField(label='Сообщение', widget=forms.Textarea(attrs={'class': 'form-control', "rows": 5}), max_length=2000)

'''
class ContactForm(ModelForm):
    class Meta:
        # Определяем модель, на основе которой создаем форму
        model = Contact
        # Поля, которые будем использовать для заполнения
        fields = ['first_name', 'last_name', 'email', 'subject', 'message']
        widgets = {
            'message': Textarea(
                attrs={
                    'placeholder': 'Напишите тут ваше сообщение'
                }
            )
        }
