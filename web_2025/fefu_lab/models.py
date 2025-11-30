from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse


class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('STUDENT', 'Студент'),
        ('TEACHER', 'Преподаватель'),
        ('ADMIN',   'Администратор'),
    ]

    FACULTY_CHOICES = [
        ('CS',  'Кибербезопасность'),
        ('SE',  'Программная инженерия'),
        ('IT',  'Информационные технологии'),
        ('DS',  'Наука о данных'),
        ('WEB', 'Веб-технологии'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='Аккаунт'
    )
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='STUDENT',
        verbose_name='Роль'
    )
    phone = models.CharField(max_length=20, blank=True, verbose_name='Телефон')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='Аватар')
    bio = models.TextField(blank=True, verbose_name='О себе')
    birth_date = models.DateField(null=True, blank=True, verbose_name='Дата рождения')
    faculty = models.CharField(
        max_length=3,
        choices=FACULTY_CHOICES,
        blank=True,
        verbose_name='Факультет'
    )
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'
        ordering = ['user__last_name', 'user__first_name']

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.get_role_display()})"

    @property
    def full_name(self):
        return self.user.get_full_name() or self.user.username

    def get_absolute_url(self):
        return reverse('profile', kwargs={'pk': self.user.pk})


class Instructor(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='instructor_profile',
        verbose_name='Преподаватель'
    )
    specialization = models.CharField(max_length=100, blank=True, verbose_name='Специализация')
    degree = models.CharField(max_length=100, blank=True, verbose_name='Учёная степень')
    is_active = models.BooleanField(default=True, verbose_name='Активен')

    class Meta:
        verbose_name = 'Преподаватель'
        verbose_name_plural = 'Преподаватели'

    def __str__(self):
        return self.user.get_full_name() or self.user.username

    @property
    def full_name(self):
        return self.user.get_full_name()


class Course(models.Model):
    LEVEL_CHOICES = [
        ('BEGINNER', 'Начальный'),
        ('INTERMEDIATE', 'Средний'),
        ('ADVANCED', 'Продвинутый'),
    ]

    title = models.CharField(max_length=200, unique=True, verbose_name='Название')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='Slug')
    description = models.TextField(verbose_name='Описание')
    duration = models.PositiveIntegerField(verbose_name='Продолжительность (часы)')
    instructor = models.ForeignKey(
        Instructor,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='courses',
        verbose_name='Преподаватель'
    )
    level = models.CharField(max_length=12, choices=LEVEL_CHOICES, default='BEGINNER', verbose_name='Уровень')
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ['title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('course', kwargs={'course_slug': self.slug})


class Enrollment(models.Model):
    STATUS_CHOICES = [
        ('ACTIVE', 'Активен'),
        ('COMPLETED', 'Завершён'),
    ]

    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='enrollments',
        verbose_name='Студент'
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='enrollments',
        verbose_name='Курс'
    )
    date_enrolled = models.DateTimeField(auto_now_add=True, verbose_name='Дата записи')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ACTIVE', verbose_name='Статус')

    class Meta:
        verbose_name = 'Запись на курс'
        verbose_name_plural = 'Записи на курсы'
        unique_together = ['student', 'course']

    def __str__(self):
        return f"{self.student} → {self.course}"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()