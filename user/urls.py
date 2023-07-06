from django.urls import path
from .views import (
    StudentRegisterView,
    StudentLoginView,
    TeachertRUDView,
    GroupRUDView,
    UserLoginView,
    TeacherRegisterView,
    TeachertLoginView,
    AssignStudentToTeacherView,
    AssignStudentToGroupView,
    AttendenceView,
    PaymentView,
    StudentProfileRUDView,
    ExpenseView,
    UserRegisterView,
)

urlpatterns = [
    path("register/user", UserRegisterView.as_view()),
    path("login/user", UserLoginView.as_view()),
    path("register/student", StudentRegisterView.as_view()),
    path("login/student", StudentLoginView.as_view()),
    path("student/get_by_id/<int:pk>", StudentProfileRUDView.as_view()),
    path("student/update_by_id/<int:pk>", StudentProfileRUDView.as_view()),
    path("student/delete_by_id/<int:pk>", StudentProfileRUDView.as_view()),
    path("student/assign_to_teacher", AssignStudentToTeacherView.as_view()),
    path("student/assign_to_group/<int:id>", AssignStudentToGroupView.as_view()),
    path("teacher/attendence", AttendenceView.as_view()),
    path("teacher/payment", PaymentView.as_view()),
    path("teacher/expense", ExpenseView.as_view()),
    path("register/teacher", TeacherRegisterView.as_view()),
    path("login/teacher", TeachertLoginView.as_view()),
    path("teacher/get_by_id/<int:pk>", TeachertRUDView.as_view()),
    path("teacher/update_by_id/<int:pk>", TeachertRUDView.as_view()),
    path("group/create", GroupRUDView.as_view()),
]
