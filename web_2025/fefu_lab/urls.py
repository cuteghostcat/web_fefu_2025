from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.about_page, name='about'),
    path('student/<int:student_id>/', views.student_profile, name='student'),
    path('course/<slug:course_slug>/', views.CourseView.as_view(), name='course'),
]

