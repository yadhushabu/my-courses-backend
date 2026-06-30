from django.contrib import admin

# Register your models here.
from .models import (
    Student, Faculty, Course, Classroom, Enrollment,
    LiveClass, StudyMaterial, Assignment, StudentMaterialCompletion
)

admin.site.register(Student)
admin.site.register(Faculty)
admin.site.register(Course)
admin.site.register(Classroom)
admin.site.register(Enrollment)
admin.site.register(LiveClass)
admin.site.register(StudyMaterial)
admin.site.register(Assignment)
admin.site.register(StudentMaterialCompletion)