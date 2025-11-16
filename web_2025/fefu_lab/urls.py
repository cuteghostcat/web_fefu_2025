from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.about_page, name='about'),
    path('student/<int:student_id>/', views.student_profile, name='student'),
    path('course/<slug:course_slug>/', views.CourseView.as_view(), name='course'),
    path('feedback/', views.feedback_view, name='feedback'),
    path('register/', views.register_student, name='register_student'),
    path('login/', views.login_view, name='login'),
    path('success/', views.success_view, name='success'),
    path('enroll/<slug:course_slug>/', views.enroll_course, name='enroll_course'),
    path('students/', views.student_list, name='student_list'),
    path('courses/', views.course_list, name='course_list'),
    path('enrollment/success/', views.enrollment_success, name='enrollment_success'),
]

