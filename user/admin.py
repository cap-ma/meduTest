from django.contrib import admin
from .models import StudentProfile, Student, Teacher, User, Group

# Register your models here.
admin.site.register(User)
admin.site.register(StudentProfile)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Group)
