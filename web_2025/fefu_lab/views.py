from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse, Http404
from django.views import View

def about_page(request):
    #return HttpResponse("Это страница \"О нас\". здесь написано о нас в с ё")
    return render(request, 'fefu_lab/about.html')

def student_profile(request, student_id):
    if student_id > 100:
        raise Http404("Студент не найден")
    #return HttpResponse(f"Профиль студента с ID: {student_id}")
    return render(request, 'fefu_lab/student.html', {'student_id': student_id})

class HomeView(View):
    def get(self, request):
        #return HttpResponse("Это есть главная страница. Самая главная страница на всём диком западе!")
        return render(request, 'fefu_lab/home.html')

class CourseView(View):
    def get(self, request, course_slug):
        if course_slug == 'unknown':
            raise Http404("Курс не найден")
        #return HttpResponse(f"Информация о курсе: {course_slug}")
        return render(request, 'fefu_lab/course.html', {'course_slug': course_slug})

def custom_404(request, exception):
    #return HttpResponse("404: Страница не найдена!", status=404)
    return render(request, 'fefu_lab/404.html', status=404)