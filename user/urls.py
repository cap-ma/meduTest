from django.urls import path
from .views import (
    StudentRegister,
    StudentLoginView,
    StudentRUD,
    TeachertRUD,
    GroupCL,
    GroupRUD,
    StudentProfileCL,
)

urlpatterns = {
    path("register/student", StudentRegister.as_view()),
    path("login/student", StudentLoginView.as_view()),
    path("student/get_by_id/<int:pk>", StudentRUD.as_view()),
    path("student/update_by_id", StudentRUD.as_view()),
    path("student/delete_by_id", StudentRUD.as_view()),
    path("studentProfile/create", StudentProfileCL.as_view()),
    path("studentProfile/get", StudentProfileCL.as_view()),
    path("student/delete_by_id", StudentRUD.as_view()),
    path("student/delete_by_id", StudentRUD.as_view()),
    path("student/delete_by_id", StudentRUD.as_view()),
    path("student/delete_by_id", StudentRUD.as_view()),
    path("teacher/get_by_id/<int:pk>", TeachertRUD.as_view()),
    path("teacher/update_by_id", TeachertRUD.as_view()),
    path("teacher/delete_by_id", TeachertRUD.as_view()),
    path("group/get_by_id/<int:pk>", GroupRUD.as_view()),
    path("group/update_by_id", GroupRUD.as_view()),
    path("group/delete_by_id", GroupRUD.as_view()),
    path("group/create", GroupCL.as_view()),
    path("group/list", GroupCL.as_view()),
}
