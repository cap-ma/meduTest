from django.shortcuts import render

from user.models import TeacherProfile, StudentProfile, User
from user.views import authenticate
from .models import (
    Test,
    TestCategory,
    OrderTestInfo,
    OrderTestInfoStudent,
    OrderTestPack,
    OrderTestPackStudent,
)


from .serializers import TestCategorySerializer, TestSerializers
from . import serializers

from rest_framework import generics
from rest_framework.views import APIView


class TestCategoryCreateView(generics.CreateAPIView):
    queryset = TestCategory.objects.all()
    serializer_class = TestCategorySerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class TestCreateView(APIView):
    def post(self, request):
        user = authenticate(request=request)

        if user:
            request.data["teacher_id"] = user.id
            serializer = TestSerializers(request)

            return Response(serializer.data, 201)


class OrderTestInfoCreateView(generics.CreateAPIView):
    queryset = OrderTestInfo.objects.all()
    serializer_class = serializers.OrderTestInfoSerializers

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
