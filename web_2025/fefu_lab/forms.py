from django import forms
from django.core.exceptions import ValidationError
from .models import UserProfile

class FeedbackForm(forms.Form):
    name = forms.CharField(max_length=100, min_length=2, label='Имя')
    email = forms.EmailField(label='Email')
    subject = forms.CharField(max_length=200, label='Тема')
    message = forms.CharField(widget=forms.Textarea, min_length=10, label='Сообщение')

    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name.strip()) < 2:
            raise ValidationError("Имя должно содержать минимум 2 символа")
        return name.strip()


class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=50, label='Логин')
    email = forms.EmailField(label='Email')
    password = forms.CharField(widget=forms.PasswordInput, min_length=8, label='Пароль')
    password_confirm = forms.CharField(widget=forms.PasswordInput, label='Подтверждение пароля')

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        if password != password_confirm:
            raise ValidationError("Пароли не совпадают!")

        username = cleaned_data.get('username')
        email = cleaned_data.get('email')
        if username and UserProfile.objects.filter(username=username).exists():
            self.add_error('username', 'Логин уже занят')
        if email and UserProfile.objects.filter(email=email).exists():
            self.add_error('email', 'Email уже зарегистрирован')

        return cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50, label='Логин')
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')
