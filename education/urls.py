from django.urls import path
from . import views

urlpatterns = [
    path("test_create", views.TestCreateView.as_view(), name="create_test"),
]
