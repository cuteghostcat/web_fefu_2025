from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.about_page, name='about'),

    path('course/<slug:course_slug>/', views.CourseView.as_view(), name='course'),
    path('courses/', views.course_list, name='course_list'),

    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('dashboard/', views.dashboard_view, name='dashboard'),
    
    path('profile/', views.profile_view, name='profile'),
    path('profile/<int:user_id>/', views.profile_view, name='profile_detail'),
    path('students/', views.student_list, name='student_list'),

    path('enroll/<slug:course_slug>/', views.enroll_course, name='enroll_course'),

    path('feedback/', views.feedback_view, name='feedback'),
]