from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin

from .models import UserProfile, Instructor, Course, Enrollment

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Профиль'
    fk_name = 'user'


class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_role')
    list_select_related = ('profile',)

    def get_role(self, instance):
        return instance.profile.get_role_display() if hasattr(instance, 'profile') else '-'
    get_role.short_description = 'Роль'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('profile')


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'user', 'specialization', 'degree', 'is_active')
    search_fields = ('user__first_name', 'user__last_name', 'user__email')
    list_filter = ('is_active',)

    def full_name(self, obj):
        return obj.full_name
    full_name.short_description = 'ФИО'


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'instructor', 'level', 'duration', 'is_active')
    list_filter = ('level', 'is_active', 'instructor')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('title',)


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'student_role', 'course', 'status', 'date_enrolled')
    list_filter = ('status', 'course__title')
    search_fields = ('student__username', 'student__email', 'student__first_name', 'student__last_name', 'course__title')
    ordering = ('-date_enrolled',)

    def student_role(self, obj):
        return obj.student.profile.get_role_display() if hasattr(obj.student, 'profile') else '—'
    student_role.short_description = 'Роль студента'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('student__profile', 'course')