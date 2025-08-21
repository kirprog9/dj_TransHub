from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from .models import *
from captcha.fields import CaptchaField


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логін', widget=forms.TextInput(attrs={'class': 'form-control', "id": "{{f.id_for_label}}"," placeholder":"username"}))
    email = forms.EmailField(label='Електронна пошта', widget=forms.TextInput(attrs={'class': 'form-control', "id": "{{f.id_for_label}}","placeholder":"email"}))
    tel = forms.CharField(label='Номер телефону', widget=forms.TextInput(
        attrs={'class': 'form-control', "id": "{{f.id_for_label}}", "placeholder": "Номер телефону"}))
    first_name = forms.CharField(label="Ім`я", widget=forms.TextInput(
        attrs={'class': 'form-control', "id": "{{f.id_for_label}}", " placeholder": "first_name"}))
    last_name = forms.CharField(label='Прізвище', widget=forms.TextInput(
        attrs={'class': 'form-control', "id": "{{f.id_for_label}}", " placeholder": "last_name"}))
    third_name = forms.CharField(label='Побатькові', widget=forms.TextInput(
        attrs={'class': 'form-control', "id": "{{f.id_for_label}}", " placeholder": "last_name"}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password', "id": "{{f.id_for_label}}","placeholder":"Password"}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password', "id": "{{f.id_for_label}}","placeholder":"Password"}))
    activity_directions = forms.ModelMultipleChoiceField(label='Напрямок праці',queryset=ActivityDirection.objects.all(),
                                                         widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}))
    role = forms.ChoiceField(label='Роль', choices=User.ROLE_CHOICES, widget=forms.Select(attrs={
        'class': 'form-control'
    }))
    name_company = forms.CharField(label='Назва вашої фірми', widget=forms.TextInput(
        attrs={'class': 'form-control', "id": "{{f.id_for_label}}", "placeholder": "Назва вашої фірми"}))


    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'tel', 'first_name', 'last_name', "third_name",
                  'password1', 'password2', "role", "name_company", "activity_directions"]
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-input'}),
            'tel': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-input'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-input'}),
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError("Цей Е-mail вже створенний, виберіть інший!")
        return email


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логін', widget=forms.TextInput(attrs={'class': 'form-control', "id": "{{f.id_for_label}}"," placeholder":"username"}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password', "id": "{{f.id_for_label}}","placeholder":"Password" }))


class ProfileUserForm(forms.ModelForm):
    username = forms.CharField(label='Логін',disabled=True, widget=forms.TextInput(
        attrs={'class': 'form-control', "id": "{{f.id_for_label}}", " placeholder": "username"}))
    email = forms.EmailField(label='Email', widget=forms.TextInput(
        attrs={'class': 'form-control', "id": "{{f.id_for_label}}", "placeholder": "email"}))
    tel = forms.CharField(label='Номер телефону', widget=forms.TextInput(
        attrs={'class': 'form-control', "id": "{{f.id_for_label}}", "placeholder": "Номер телефону"}))
    first_name = forms.CharField(label='Имя', widget=forms.TextInput(
        attrs={'class': 'form-control', "id": "{{f.id_for_label}}", " placeholder": "first_name"}))
    last_name = forms.CharField(label='Фамилия', widget=forms.TextInput(
        attrs={'class': 'form-control', "id": "{{f.id_for_label}}", " placeholder": "last_name"}))
    third_name = forms.CharField(label='Отчество',required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', "id": "{{f.id_for_label}}", " placeholder": "last_name"}))
    about = forms.CharField(label='О себе',required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', "id": "{{f.id_for_label}}", " placeholder": "about"}))
    activity_directions = forms.ModelMultipleChoiceField(label='Напрямок праці',
                                                         queryset=ActivityDirection.objects.all(),
                                                         widget=forms.CheckboxSelectMultiple(
                                                             attrs={'class': 'form-check-input'}))
    role = forms.ChoiceField(label='Роль', choices=User.ROLE_CHOICES, widget=forms.Select(attrs={
        'class': 'form-control'
    }))
    name_company = forms.CharField(label='Назва вашої фірми', widget=forms.TextInput(
        attrs={'class': 'form-control', "id": "{{f.id_for_label}}", "placeholder": "Назва вашої фірми"}))
    photo = forms.ImageField(widget=forms.ClearableFileInput)

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'tel', 'first_name', 'last_name', "third_name",
                  'about', "role", 'photo', "name_company", "activity_directions"]


    def clean_email(self):
        email = self.cleaned_data['email']
        username = self.cleaned_data['username']
        user = User.objects.get(username=username)
        email2 = user.email
        if get_user_model().objects.filter(email=email).exists():
            if email==email2:
                return email
            else:
                raise forms.ValidationError("Цей Е-mail вже створенний, виберіть інший!")
        return email


class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label="Старий пароль", widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    new_password1 = forms.CharField(label="Новий пароль", widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    new_password2 = forms.CharField(label="Підтверждення пароля", widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ['target_user', 'rating', 'comment']
        widgets = {
            'target_user': forms.Select(attrs={'class': 'form-control', 'id': 'target_user'}),
            'rating': forms.Select(attrs={
                'class': 'form-control',
                'id': 'review_rating'
            }, choices=[(i, i) for i in range(1, 6)]),  # Assuming a 5-star rating system
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Напишіть свій відгук тут...',
                'id': 'review_content'
            }),
        }

    def __init__(self, *args, **kwargs):
        current_user = kwargs.pop('current_user', None)
        super().__init__(*args, **kwargs)
        if current_user:
            self.fields['target_user'].queryset = User.objects.exclude(pk=current_user.pk)


class ComplaintForm(forms.ModelForm):

    class Meta:
        model = Complaint
        fields = ['target_user', 'description']

        widgets = {
            'target_user': forms.Select(attrs={'class': 'form-control', 'id': 'target_user'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Напишіть свою скаргу тут...',
                'id': 'review_content'})
        }

    def __init__(self, *args, **kwargs):
        current_user = kwargs.pop('current_user', None)
        super().__init__(*args, **kwargs)
        if current_user:
            self.fields['target_user'].queryset = User.objects.exclude(pk=current_user.pk)