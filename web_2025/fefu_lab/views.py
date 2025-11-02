from django.shortcuts import render, redirect

# Create your views here.

from django.contrib import messages
from django.http import HttpResponse, Http404
from django.views import View
from .forms import FeedbackForm, RegistrationForm, LoginForm
from .models import UserProfile

def about_page(request):
    #return HttpResponse("Это страница \"О нас\". здесь написано о нас в с ё")
    return render(request, 'fefu_lab/about.html')


class HomeView(View):
    def get(self, request):
        #return HttpResponse("Это есть главная страница. Самая главная страница на всём диком западе!")
        return render(request, 'fefu_lab/home.html')


def custom_404(request, exception):
    #return HttpResponse("404: Страница не найдена!", status=404)
    return render(request, 'fefu_lab/404.html', status=404)

def student_profile(request, student_id):
    if student_id in STUDENTS_DATA:
        student_data = STUDENTS_DATA[student_id]
        return render(request, 'fefu_lab/student_profile.html', {
            'student_id': student_id,
            'student_info': student_data['info'],
            'faculty': student_data['faculty'],
            'status': student_data['status'],
            'year': student_data['year']
        })
    else:
        raise Http404("Студент с таким ID не найден")

class CourseView(View):
    def get(self, request, course_slug):
        if course_slug not in COURSES_DATA:
            raise Http404("Курс не найден")
        data = COURSES_DATA[course_slug]
        return render(request, 'fefu_lab/course_detail.html', {
            'course_slug': course_slug,
            'name': data['name'],
            'duration': data['duration'],
            'description': data['description'],
            'instructor': data['instructor'],
            'level': data['level'],
        })

def feedback_view(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Сообщение отправлено!')
            return redirect('success')
    else:
        form = FeedbackForm()
    return render(request, 'fefu_lab/feedback.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            UserProfile.objects.create(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']  # В реальности — хэш!
            )
            messages.success(request, 'Регистрация успешна!')
            return redirect('success')
    else:
        form = RegistrationForm()
    return render(request, 'fefu_lab/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Вход выполнен!')
            return redirect('success')
    else:
        form = LoginForm()
    return render(request, 'fefu_lab/login.html', {'form': form})

def success_view(request):
    return render(request, 'fefu_lab/success.html')

STUDENTS_DATA = {
    1: {
        'info': 'Иван Петров',
        'faculty': 'Кибербезопасность',
        'status': 'Активный',
        'year': 3
    },
    2: {
        'info': 'Мария Сидорова', 
        'faculty': 'Информатика',
        'status': 'Активный',
        'year': 2
    },
    3: {
        'info': 'Алексей Козлов',
        'faculty': 'Программная инженерия', 
        'status': 'Выпускник',
        'year': 5
    }
}

COURSES_DATA = {
    'python-basics': {
        'name': 'Основы программирования на Python',
        'duration': 36,
        'description': 'Базовый курс по программированию на языке Python для начинающих.',
        'instructor': 'Доцент Петров И.С.',
        'level': 'Начальный'
    },
    'web-security': {
        'name': 'Веб-безопасность',
        'duration': 48,
        'description': 'Курс по защите веб-приложений от современных угроз.',
        'instructor': 'Профессор Сидоров А.В.',
        'level': 'Продвинутый'
    },
    'network-defense': {
        'name': 'Защита сетей',
        'duration': 42,
        'description': 'Изучение методов и технологий защиты компьютерных сетей.',
        'instructor': 'Доцент Козлова М.П.',
        'level': 'Средний'
    }
}