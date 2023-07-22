from django.urls import path
from . import views

urlpatterns = [
    path("test_create", views.TestCreateView.as_view(), name="create_test"),
    path(
        "test_category_create",
        views.TestCategoryCreateView.as_view(),
        name="create_test_category",
    ),
    path(
        "order_test_create",
        views.OrderTestInfoCreateView.as_view(),
        name="order_test_create",
    ),
    path(
        "order_test_assign_student",
        views.OrderTestInfoStudentAssignView.as_view(),
        name="assign_student",
    ),
]
