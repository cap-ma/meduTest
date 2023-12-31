from django.urls import path
from . import views

urlpatterns = [

    path("test/list", views.TestListView.as_view()),
    path("test/list/for_teacher", views.TestListView.as_view()),
    path("test/update/<int:pk>", views.TestUDView.as_view()),
    path("test/delete/<int:pk>", views.TestUDView.as_view()),


    path("test_category/list", views.TestCategoryListView.as_view()),
    path("tests_category_based", views.TestGetCategory.as_view()),
    path("test_create", views.TestCreateView.as_view(), name="create_test"),


    path("get_category/<int:id>", views.TestGetCategoryById.as_view()),
    path(
        "test_category_create",
        views.TestCategoryCreateView.as_view(),
        name="create_test_category",
    ),
    path(
        "test_category/update/<int:pk>",
        views.TestCategoryUDView.as_view(),
        name="update_test_category",
    ),
    path(
        "test_category/delete/<int:pk>",
        views.TestCategoryUDView.as_view(),
        name="delete_test_category",
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

    path("order_test_pack_results", views.OrderTestPackStudentResultView.as_view()),##check later 


    path("order_test_pack/list", views.OrderTestPackListView.as_view()),##check later

    path("order_test_info/list", views.OrderTestInfoListView.as_view()),#checked
    path("order_test_info_test/<int:id>", views.GetOrderTestInfoTestPackView.as_view()),#checked
    path("total_test_count",views.TotalTestCountView.as_view()),#checked
   
    path("order_test_info_detail",views.OrderTestInfoGetTeacherView.as_view()),#checked

    path("order_test_info_assigned_student_results",views.GetTeacherTestInfoStudentResultsView.as_view()),

    ###########STUDENT######
    path("order_test_infos_of_assigned_student",views.OrderTestinfoAssignedStudentsView.as_view()),
    path("order_test_infos_of_assigned_student/<int:id>",views.TestInfoDetailForStudentView.as_view())
]
