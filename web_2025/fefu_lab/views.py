from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404
from django.views import View
from django.db import IntegrityError

from .forms import RegisterForm, LoginForm, FeedbackForm, EnrollmentForm
from .models import Course, Instructor, Enrollment, UserProfile
from django.contrib.auth.models import User

class HomeView(View):
    def get(self, request):
        try:
            total_students = UserProfile.objects.filter(role='STUDENT', is_active=True).count()
            total_courses = Course.objects.filter(is_active=True).count()
            total_instructors = Instructor.objects.filter(is_active=True).count()
            recent_courses = Course.objects.filter(is_active=True).order_by('-created_at')[:3]
        except Exception as e:
            raise Http404(f"Ошибка загрузки данных: {e}")

        context = {
            'total_students': total_students,
            'total_courses': total_courses,
            'total_instructors': total_instructors,
            'recent_courses': recent_courses,
        }
        return render(request, 'fefu_lab/home.html', context)


def about_page(request):
    return render(request, 'fefu_lab/about.html')


class CourseView(View):
    def get(self, request, course_slug):
        course = get_object_or_404(Course, slug=course_slug, is_active=True)
        return render(request, 'fefu_lab/course_detail.html', {'course': course})


@login_required
def profile_view(request, user_id=None):
    if user_id:
        profile_user = get_object_or_404(User, pk=user_id)
    else:
        profile_user = request.user

    return render(request, 'fefu_lab/profile.html', {'profile_user': profile_user})

@login_required
def dashboard_view(request):
    profile = request.user.profile

    if profile.role == 'TEACHER':
        courses = Course.objects.filter(instructor__user=request.user).prefetch_related('enrollments')
        
        for course in courses:
            course.active_enrollments = course.enrollments.filter(status='ACTIVE').count()
            course.total_enrollments = course.enrollments.count()

        return render(request, 'fefu_lab/dashboard/teacher.html', {
            'courses': courses
        })

    elif profile.role == 'ADMIN':
        return render(request, 'fefu_lab/dashboard/admin.html')

    else:  
        enrollments = request.user.enrollments.select_related('course').filter(status='ACTIVE')
        return render(request, 'fefu_lab/dashboard/student.html', {
            'enrollments': enrollments
        })


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # ← ВОТ ЭТА СТРОЧКА — главное исправление!
            login(request, user, backend='fefu_lab.backends.EmailBackend')
            messages.success(request, f'Добро пожаловать, {user.first_name}!')
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'fefu_lab/registration/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'С возвращением, {user.first_name}!')
                return redirect('dashboard')
            else:
                messages.error(request, 'Неверный email или пароль')
    else:
        form = LoginForm()
    return render(request, 'fefu_lab/registration/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'Вы успешно вышли из аккаунта')
    return redirect('home')


@login_required
def enroll_course(request, course_slug):
    course = get_object_or_404(Course, slug=course_slug, is_active=True)

    if Enrollment.objects.filter(student=request.user, course=course).exists():
        messages.info(request, 'Вы уже записаны на этот курс')
        return redirect('course', course_slug=course.slug)

    if request.method == 'POST':
        form = EnrollmentForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Вы успешно записались на курс "{course.title}"!')
            return redirect('dashboard')
    else:
        form = EnrollmentForm(user=request.user, initial={'course': course})

    return render(request, 'fefu_lab/enrollment.html', {
        'form': form,
        'course': course
    })


def feedback_view(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Спасибо за обратную связь!')
            return redirect('home')
    else:
        form = FeedbackForm()
    return render(request, 'fefu_lab/feedback.html', {'form': form})


def custom_404(request, exception):
    return render(request, 'fefu_lab/404.html', status=404)


def course_list(request):
    courses = Course.objects.filter(is_active=True).order_by('title')
    return render(request, 'fefu_lab/course_list.html', {'courses': courses})

def student_list(request):
    students = UserProfile.objects.filter(
        role='STUDENT',
        is_active=True,
        user__is_active=True
    ).select_related('user').order_by('user__last_name', 'user__first_name')

    return render(request, 'fefu_lab/student_list.html', {
        'students': students
    })
