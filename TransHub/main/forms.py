from django import forms
from .models import *
from captcha.fields import CaptchaField


class ContactForm(forms.Form):
    name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Електронна пошта', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    content = forms.CharField(label='Текст',widget=forms.Textarea(attrs={'class': 'form-input'}))


