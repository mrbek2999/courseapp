from django.contrib import admin
from .models import Student, Teacher, Course, CustomUser


admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Course)
admin.site.register(CustomUser)
