from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UsersAPIView, TeachersViewSet, CustomAuthToken, TeachersUnApproveAPIView, StudentCoursesAPIView, \
    StudentsViewSet, TeacherSaveViewSet, StudentSaveViewSet, TeacherCoursesAPIView, CoursesViewSet, Logout

router = DefaultRouter()
router.register('teachers', TeachersViewSet)
router.register('teacher-save', TeacherSaveViewSet)
router.register('students', StudentsViewSet)
router.register('student-save', StudentSaveViewSet)
router.register('courses', CoursesViewSet)

urlpatterns = [
    path('users/', UsersAPIView.as_view(), name='users'),
    path('teachers-unapprove/', TeachersUnApproveAPIView.as_view()),
    path('student-courses/<int:pk>', StudentCoursesAPIView.as_view()),
    path('teacher-courses/<int:pk>', TeacherCoursesAPIView.as_view()),
    path('', include(router.urls)),
    path('login/', CustomAuthToken.as_view()),
    path('logout/', Logout.as_view()),
]
