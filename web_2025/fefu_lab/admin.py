from django.contrib import admin

from .models import Student, Instructor, Course, Enrollment

# Register your models here.

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'faculty', 'birth_date', 'is_active', 'created_at')
    list_filter = ('faculty', 'is_active')
    search_fields = ('first_name', 'last_name', 'email')
    ordering = ('last_name', 'first_name')
    fields = ('first_name', 'last_name', 'email', 'birth_date', 'faculty', 'is_active')  # Поля в форме редактирования

@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'specialization', 'degree', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('first_name', 'last_name', 'email')
    ordering = ('last_name', 'first_name')

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'instructor', 'level', 'duration', 'is_active', 'created_at')
    list_filter = ('level', 'is_active')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}  # Авто-генерация slug
    ordering = ('title',)

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'status', 'date_enrolled')
    list_filter = ('status',)
    search_fields = ('student__last_name', 'course__title')
    ordering = ('-date_enrolled',)