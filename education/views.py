from django.shortcuts import render
from user.models import TeacherProfile, StudentProfile, User
from .serializers import TestCategorySerializer, TestSerializers
from rest_framework import generics
from . import serializers
from .models import (
    Test,
    TestCategory,
    OrderTestInfo,
    OrderTestInfoStudent,
    OrderTestPack,
    OrderTestPackStudent,
)


class TestCategoryCreateView(generics.CreateAPIView):
    queryset = TestCategory.objects.all()
    serializer_class = TestCategorySerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class TestCreateView(generics.CreateAPIView):
    queryset = Test.objects.all()
    serializer_class = TestSerializers

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class OrderTestInfoCreateView(generics.CreateAPIView):
    queryset = OrderTestInfo.objects.all()
    serializer_class = serializers.OrderTestInfoSerializers

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
