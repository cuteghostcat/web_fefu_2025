from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from .models import UserProfile, Enrollment, Course


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


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')
    first_name = forms.CharField(max_length=30, required=True, label='Имя')
    last_name = forms.CharField(max_length=30, required=True, label='Фамилия')
    phone = forms.CharField(max_length=20, required=False, label='Телефон')
    faculty = forms.CharField(max_length=100, required=False, label='Факультет')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'phone', 'faculty', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Этот email уже зарегистрирован.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            profile = user.profile
            profile.phone = self.cleaned_data.get('phone', '')
            profile.faculty = self.cleaned_data.get('faculty', '')
            profile.save()
        return user


class LoginForm(forms.Form):
    email = forms.EmailField(label='Email')
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')


class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['course']

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        if 'course' in self.fields:
            self.fields['course'].widget = forms.HiddenInput()

    def clean(self):
        cleaned_data = super().clean()
        course = cleaned_data.get('course')
        if course and self.user:
            if Enrollment.objects.filter(student=self.user, course=course).exists():
                raise forms.ValidationError("Вы уже записаны на этот курс!")
        return cleaned_data

    def save(self, commit=True):
        enrollment = super().save(commit=False)
        enrollment.student = self.user
        if commit:
            enrollment.save()
        return enrollment