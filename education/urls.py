from django.urls import path
from . import views

urlpatterns = [
    path("test/list", views.TestListView.as_view()),
    path("test_category/list", views.TestCategoryListView.as_view()),
    path("tests_category_based/<int:category_id>", views.TestGetCategory.as_view()),
    path("test_create", views.TestCreateView.as_view(), name="create_test"),
    path("test_category_get", views.TestCategoryCreateView.as_view()),
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
    path("order_test_pack_results", views.OrderTestPackStudentResultView.as_view()),
    path("order_test_pack/list", views.OrderTestPackListView.as_view()),
    path("order_test_info/list", views.OrderTestInfoView.as_view()),
    path("order_test_info_test/<int:id>", views.GetOrderTestInfoTestPackView.as_view()),
]
