from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    is_teacher = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.username}'


class Student(models.Model):
    first_name = models.CharField(max_length=512, null=True, blank=True)
    last_name = models.CharField(max_length=512, null=True, blank=True)
    username = models.CharField(max_length=512)
    email = models.EmailField(null=True, blank=True)
    password = models.CharField(max_length=256)
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.username}'


class Teacher(models.Model):
    first_name = models.CharField(max_length=512, null=True, blank=True)
    last_name = models.CharField(max_length=512, null=True, blank=True)
    username = models.CharField(max_length=512)
    email = models.EmailField(null=True, blank=True)
    password = models.CharField(max_length=256)
    is_active = models.BooleanField(default=False)
    is_approve = models.BooleanField(default=True)
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, null=True, blank=True)
    course = models.ManyToManyField('Course', null=True, blank=True)

    def __str__(self):
        return f'{self.username}'


class Course(models.Model):
    photo = models.ImageField(upload_to='media/courses/')
    desc = models.TextField()
    price = models.CharField(max_length=256)
    title = models.CharField(max_length=512)
    student = models.ManyToManyField(to='Student', related_name='students')

    def __str__(self):
        return f'{self.title}'
