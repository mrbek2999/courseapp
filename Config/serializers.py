from rest_framework import serializers
from .models import CustomUser, Teacher, Course, Student


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'first_name', 'last_name', 'username')


class StudentsSerializer(serializers.ModelSerializer):
    user = UsersSerializer()

    class Meta:
        model = Student
        fields = ('id', 'first_name', 'last_name', 'username', 'user')


class SaveStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('first_name', 'last_name', 'username', 'password', 'email')


class CourseSerializer(serializers.ModelSerializer):
    student = StudentsSerializer(many=True)

    class Meta:
        model = Course
        fields = ('id', 'photo', 'title', 'price', 'student')


class TeachersSerializer(serializers.ModelSerializer):
    course = CourseSerializer(many=True)

    class Meta:
        model = Teacher
        fields = ('id', 'first_name', 'last_name', 'course', 'is_active', 'is_approve')


class SaveTeachersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ('first_name', 'last_name', 'username', 'password', 'email')
