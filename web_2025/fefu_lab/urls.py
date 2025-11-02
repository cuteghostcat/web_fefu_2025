from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.about_page, name='about'),
    path('student/<int:student_id>/', views.student_profile, name='student'),
    path('course/<slug:course_slug>/', views.CourseView.as_view(), name='course'),
    path('feedback/', views.feedback_view, name='feedback'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('success/', views.success_view, name='success'),
]

