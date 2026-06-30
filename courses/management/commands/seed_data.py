from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from courses.models import (
    Student, Faculty, Course, Classroom, Enrollment,
    LiveClass, StudyMaterial, Assignment, StudentMaterialCompletion
)


class Command(BaseCommand):
    help = 'Seeds the database with realistic sample data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Clearing old data...')
        StudentMaterialCompletion.objects.all().delete()
        Assignment.objects.all().delete()
        StudyMaterial.objects.all().delete()
        LiveClass.objects.all().delete()
        Enrollment.objects.all().delete()
        Classroom.objects.all().delete()
        Course.objects.all().delete()
        Faculty.objects.all().delete()
        Student.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()

        self.stdout.write('Creating faculty...')
        # Lekshmi R -> Python, Data Science
        # Hashim H  -> Python, React
        # Adit S    -> Data Analytics
        fac_user_lekshmi = User.objects.create_user('lekshmi_r', password='faculty123', first_name='Lekshmi', last_name='R')
        fac_user_hashim = User.objects.create_user('hashim_h', password='faculty123', first_name='Hashim', last_name='H')
        fac_user_adit = User.objects.create_user('adit_s', password='faculty123', first_name='Adit', last_name='S')

        faculty_lekshmi = Faculty.objects.create(user=fac_user_lekshmi, designation='Senior Instructor')
        faculty_hashim = Faculty.objects.create(user=fac_user_hashim, designation='Lead Instructor')
        faculty_adit = Faculty.objects.create(user=fac_user_adit, designation='Instructor')

        self.stdout.write('Creating students...')
        stu_user1 = User.objects.create_user('arya_r', password='student123', first_name='Arya', last_name='R')
        stu_user2 = User.objects.create_user('govind_g', password='student123', first_name='Govind', last_name='G')
        student1 = Student.objects.create(user=stu_user1, roll_number='STU001')
        student2 = Student.objects.create(user=stu_user2, roll_number='STU002')

        self.stdout.write('Creating courses...')
        # Python -> taught jointly by Lekshmi and Hashim
        course1 = Course.objects.create(title='Python for Beginners', description='Core Python fundamentals')
        course1.faculty.add(faculty_lekshmi, faculty_hashim)

        # Data Science -> Lekshmi
        course2 = Course.objects.create(title='Data Science Essentials', description='Statistics, pandas, and ML foundations')
        course2.faculty.add(faculty_lekshmi)

        # React -> Hashim
        course3 = Course.objects.create(title='React Fundamentals', description='Modern frontend with React')
        course3.faculty.add(faculty_hashim)

        # Data Analytics -> Adit
        course4 = Course.objects.create(title='Data Analytics', description='Data wrangling, visualisation, and reporting')
        course4.faculty.add(faculty_adit)
        # course4 deliberately has NO materials added below — edge case

        self.stdout.write('Creating classrooms...')
        classroom1 = Classroom.objects.create(name='Python Batch A', course=course1)
        classroom2 = Classroom.objects.create(name='Data Science Batch A', course=course2)
        classroom3 = Classroom.objects.create(name='React Batch A', course=course3)
        # Note: no classroom created for course4 — student will be enrolled but unassigned

        self.stdout.write('Creating enrollments...')
        # arya_r: enrolled in course1 (assigned), course2 (assigned), course4 (NOT assigned - edge case)
        Enrollment.objects.create(student=student1, course=course1, classroom=classroom1)
        Enrollment.objects.create(student=student1, course=course2, classroom=classroom2)
        Enrollment.objects.create(student=student1, course=course4, classroom=None)

        # govind_g: enrolled in course1 (assigned), course3 (assigned)
        Enrollment.objects.create(student=student2, course=course1, classroom=classroom1)
        Enrollment.objects.create(student=student2, course=course3, classroom=classroom3)

        self.stdout.write('Creating live classes...')
        now = timezone.now()
        LiveClass.objects.create(course=course1, title='Intro to Variables', scheduled_at=now + timedelta(days=1), meeting_link='https://meet.example.com/abc1')
        LiveClass.objects.create(course=course1, title='Loops and Functions', scheduled_at=now + timedelta(days=3), meeting_link='https://meet.example.com/abc2')
        LiveClass.objects.create(course=course2, title='Intro to Pandas', scheduled_at=now + timedelta(days=2), meeting_link='https://meet.example.com/abc3')
        LiveClass.objects.create(course=course3, title='React Hooks Deep Dive', scheduled_at=now + timedelta(days=4), meeting_link='https://meet.example.com/abc4')
        # course4 has no live classes scheduled yet — also fine, naturally sparse

        self.stdout.write('Creating study materials...')
        m1 = StudyMaterial.objects.create(course=course1, folder='Week 1', title='Python Basics Slides', file_url='https://example.com/slides1.pdf')
        m2 = StudyMaterial.objects.create(course=course1, folder='Week 1', title='Variables Cheat Sheet', file_url='https://example.com/cheatsheet1.pdf')
        m3 = StudyMaterial.objects.create(course=course1, folder='Week 2', title='Functions Notes', file_url='https://example.com/notes1.pdf')

        m4 = StudyMaterial.objects.create(course=course2, folder='Module 1', title='Pandas Overview', file_url='https://example.com/ds1.pdf')
        m5 = StudyMaterial.objects.create(course=course2, folder='Module 1', title='Statistics Primer', file_url='https://example.com/ds2.pdf')

        m6 = StudyMaterial.objects.create(course=course3, folder='Basics', title='JSX Introduction', file_url='https://example.com/react1.pdf')
        # course4 ('Data Analytics') intentionally has ZERO materials — edge case from the task

        self.stdout.write('Creating assignments...')
        Assignment.objects.create(course=course1, title='Variables Exercise', due_date=now + timedelta(days=5), status='published')
        Assignment.objects.create(course=course1, title='Loops Mini-Project', due_date=now - timedelta(days=2), status='submitted')
        Assignment.objects.create(course=course2, title='Pandas Practice Set', due_date=now - timedelta(days=5), status='evaluated')
        Assignment.objects.create(course=course2, title='Stats Take-Home', due_date=now + timedelta(days=7), status='published')
        Assignment.objects.create(course=course3, title='Build a Counter App', due_date=now - timedelta(days=1), status='submitted')

        self.stdout.write('Marking some materials complete...')
        # arya_r completed 2 out of 3 materials in course1 -> partial progress
        StudentMaterialCompletion.objects.create(student=student1, material=m1)
        StudentMaterialCompletion.objects.create(student=student1, material=m2)
        # m3 left incomplete deliberately

        # arya_r completed both materials in course2 -> full progress
        StudentMaterialCompletion.objects.create(student=student1, material=m4)
        StudentMaterialCompletion.objects.create(student=student1, material=m5)

        # govind_g hasn't completed anything in course1 -> zero progress
        # govind_g hasn't touched course3 materials either -> zero progress

        self.stdout.write(self.style.SUCCESS('Seed data created successfully!'))
        self.stdout.write(f'Student 1 login: arya_r / student123')
        self.stdout.write(f'Student 2 login: govind_g / student123')