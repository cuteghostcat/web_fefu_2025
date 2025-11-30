from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from fefu_lab.models import UserProfile, Instructor, Course, Enrollment
from datetime import date


class Command(BaseCommand):
    help = 'Заполняет базу данных тестовыми данными (обновлено под лабу №4)'

    def handle(self, *args, **options):
        self.stdout.write('Очистка старых данных...')
        Enrollment.objects.all().delete()
        Course.objects.all().delete()
        Instructor.objects.all().delete()
        UserProfile.objects.all().delete()
        User.objects.filter(is_staff=False, is_superuser=False).delete()  

        self.stdout.write('Создание преподавателей...')

        teacher1 = User.objects.create_user(
            username='i.petrov',
            email='i.petrov@fefu.ru',
            password='teacher123',
            first_name='Иван',
            last_name='Петров'
        )
        Instructor.objects.create(
            user=teacher1,
            specialization='Кибербезопасность',
            degree='Кандидат технических наук'
        )

        teacher2 = User.objects.create_user(
            username='m.sidorova',
            email='m.sidorova@fefu.ru',
            password='teacher123',
            first_name='Мария',
            last_name='Сидорова'
        )
        Instructor.objects.create(
            user=teacher2,
            specialization='Веб-разработка',
            degree='Доктор технических наук'
        )

        teacher3 = User.objects.create_user(
            username='a.kozlov',
            email='a.kozlov@fefu.ru',
            password='teacher123',
            first_name='Алексей',
            last_name='Козлов'
        )
        Instructor.objects.create(
            user=teacher3,
            specialization='Сетевые технологии'
        )

        instructors = [teacher1, teacher2, teacher3]

        self.stdout.write('Создание студентов...')

        student_data = [
            ('Анна', 'Иванова', 'anna.ivanova@fefu.ru', date(2000, 5, 15), 'CS'),
            ('Дмитрий', 'Смирнов', 'dmitry.smirnov@fefu.ru', date(1999, 8, 22), 'SE'),
            ('Екатерина', 'Попова', 'ekaterina.popova@fefu.ru', date(2001, 3, 10), 'IT'),
            ('Михаил', 'Васильев', 'mikhail.vasilyev@fefu.ru', date(2000, 11, 5), 'DS'),
            ('Ольга', 'Новикова', 'olga.novikova@fefu.ru', date(1999, 12, 30), 'WEB'),
        ]

        students = []
        for first_name, last_name, email, birth_date, faculty in student_data:
            user = User.objects.create_user(
                username=email.split('@')[0],
                email=email,
                password='student123',
                first_name=first_name,
                last_name=last_name
            )
            profile, created = UserProfile.objects.get_or_create(user=user)
            profile.birth_date = birth_date
            profile.faculty = faculty
            profile.role = 'STUDENT'
            profile.save()
            students.append(user)

        self.stdout.write('Создание курсов...')

        courses = [
            Course(
                title='Основы Python',
                slug='python-basics',
                description='Базовый курс по программированию на языке Python.',
                duration=36,
                instructor=Instructor.objects.get(user=teacher1),
                level='BEGINNER',
            ),
            Course(
                title='Веб-безопасность',
                slug='web-security',
                description='Продвинутый курс по защите веб-приложений.',
                duration=48,
                instructor=Instructor.objects.get(user=teacher1),
                level='ADVANCED',
            ),
            Course(
                title='Современный JavaScript',
                slug='modern-javascript',
                description='ES6+, асинхронность, фреймворки.',
                duration=42,
                instructor=Instructor.objects.get(user=teacher2),
                level='INTERMEDIATE',
            ),
            Course(
                title='Защита сетей',
                slug='network-defense',
                description='Firewalls, IDS/IPS, VPN, атаки.',
                duration=40,
                instructor=Instructor.objects.get(user=teacher3),
                level='ADVANCED',
            ),
        ]

        for course in courses:
            course.save()

        self.stdout.write('Создание записей на курсы...')

        enrollments = [
            (students[0], courses[0]),  
            (students[0], courses[1]),  
            (students[1], courses[0]),  
            (students[1], courses[2]),  
            (students[2], courses[0]),  
            (students[3], courses[3]),  
            (students[4], courses[2]),  
        ]

        for student_user, course in enrollments:
            Enrollment.objects.create(
                student=student_user,
                course=course,
                status='ACTIVE'
            )

        self.stdout.write(self.style.SUCCESS(
            f'Готово! Создано:\n'
            f'   • {len(instructors)} преподавателей\n'
            f'   • {len(students)} студентов\n'
            f'   • {len(courses)} курсов\n'
            f'   • {len(enrollments)} записей на курсы\n'
            f'Логин: любой email, пароль: student123 / teacher123'
        ))