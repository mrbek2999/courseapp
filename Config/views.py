from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .models import CustomUser, Teacher, Course, Student
from .serializers import UsersSerializer, TeachersSerializer, CourseSerializer, StudentsSerializer, \
    SaveTeachersSerializer, SaveStudentSerializer


class UsersAPIView(APIView):
    def get(self, request):
        users = CustomUser.objects.all()
        serializer = UsersSerializer(users, many=True)
        return Response(data=serializer.data)


class StudentCoursesAPIView(APIView):
    def get(self, request, pk):
        courses = Course.objects.filter(student__user__pk=pk)
        serializer = CourseSerializer(courses, many=True)
        return Response(data=serializer.data)


class TeacherCoursesAPIView(APIView):
    def get(self, request, pk):
        teacher = Teacher.objects.get(user__pk=pk)
        serializer = TeachersSerializer(teacher)
        return Response(data=serializer.data)


class TeachersUnApproveAPIView(APIView):
    def get(self, request):
        teachers = Teacher.objects.filter(is_approve=True).filter(is_active=False)
        serializer = TeachersSerializer(teachers, many=True)
        return Response(data=serializer.data)


class TeachersViewSet(ModelViewSet):
    queryset = Teacher.objects.all()
    authentication_classes = (TokenAuthentication,)
    serializer_class = TeachersSerializer


class TeacherSaveViewSet(ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = SaveTeachersSerializer


class StudentsViewSet(ModelViewSet):
    queryset = Student.objects.all()
    authentication_classes = (TokenAuthentication,)
    serializer_class = StudentsSerializer


class AllCoursesViewSet(ReadOnlyModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class CoursesViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(student=[])
        teacher = Teacher.objects.get(user=self.request.user)
        course = Course.objects.get(id=serializer.data['id'])
        teacher.course.add(course.pk)


class StudentSaveViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = SaveStudentSerializer


class CustomAuthToken(ObtainAuthToken):
    def get(self, request):
        return Response(status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'is_superuser': user.is_superuser,
            'is_teacher': user.is_teacher,
            'is_student': user.is_student
        })


class Logout(APIView):
    def post(self, request):
        Token.objects.filter(key=request.data['token']).delete()
        return Response(status=status.HTTP_200_OK)
