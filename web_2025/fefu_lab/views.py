from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.

from django.contrib import messages
from django.http import HttpResponse, Http404
from django.views import View
from .forms import FeedbackForm, RegistrationForm, LoginForm
from .models import UserProfile
from .models import Student, Course, Instructor, Enrollment
from .forms import StudentRegistrationForm, EnrollmentForm

def about_page(request):
    #return HttpResponse("Это страница \"О нас\". здесь написано о нас в с ё")
    return render(request, 'fefu_lab/about.html')


class HomeView(View):
    def get(self, request):
        try:
            total_students = Student.objects.filter(is_active=True).count()
            total_courses = Course.objects.filter(is_active=True).count()
            total_instructors = Instructor.objects.filter(is_active=True).count()
            recent_courses = Course.objects.filter(is_active=True).order_by('-created_at')[:3]
        except Exception as e:
            raise Http404("Ошибка при загрузке данных: " + str(e))

        return render(request, 'fefu_lab/home.html', {
            'total_students': total_students,
            'total_courses': total_courses,
            'total_instructors': total_instructors,
            'recent_courses': recent_courses
        })


def custom_404(request, exception):
    #return HttpResponse("404: Страница не найдена!", status=404)
    return render(request, 'fefu_lab/404.html', status=404)

def student_profile(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    return render(request, 'fefu_lab/student_detail.html', {'student': student})

class CourseView(View):
    def get(self, request, course_slug):
        course = get_object_or_404(Course, slug=course_slug)
        return render(request, 'fefu_lab/course_detail.html', {'course': course})

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

def register_student(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # Или на профиль
    else:
        form = StudentRegistrationForm()
    return render(request, 'fefu_lab/register.html', {'form': form})

def enroll_course(request, course_slug):
    course = get_object_or_404(Course, slug=course_slug)
    
    if request.method == 'POST':
        form = EnrollmentForm(request.POST, initial={'course': course})
        if form.is_valid():
            enrollment = form.save(commit=False)
            enrollment.course = course  # Устанавливаем курс
            try:
                enrollment.save()
                messages.success(request, 'Запись на курс успешна!')
                return redirect('enrollment_success')  # Перенаправление на success
            except IntegrityError:
                messages.error(request, 'Вы уже записаны на этот курс или произошла ошибка.')
    else:
        form = EnrollmentForm(initial={'course': course})
    
    return render(request, 'fefu_lab/enrollment.html', {'form': form, 'course': course})

def enrollment_success(request):
    return render(request, 'fefu_lab/enrollment_success.html')

def student_list(request):
    students = Student.objects.filter(is_active=True).order_by('last_name', 'first_name')
    return render(request, 'fefu_lab/student_list.html', {'students': students})

def course_list(request):
    courses = Course.objects.filter(is_active=True).order_by('title')
    return render(request, 'fefu_lab/course_list.html', {'courses': courses})
