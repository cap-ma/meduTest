from django.shortcuts import render
from rest_framework.response import Response
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
import random


from .serializers import (
    TestCategorySerializer,
    TestSerializers,
    OrderTestPackSerializers,
    OrderTestPackResponseSerializers,
    OrderTestPackStudentsSerializer,
)
from . import serializers
from rest_framework import generics
from rest_framework.views import APIView


class TestCategoryCreateView(APIView):
    def post(self, request):
        user = authenticate(request=request)

        if user.role == "TEACHER":
            test_category = TestCategory.objects.create(
                title=request.data["title"],
                teacher=user.teacher_profile,
            )

            serializer = TestCategorySerializer(test_category)

            return Response(serializer.data, 201)


class TestCreateView(APIView):
    def post(self, request):
        user = authenticate(request=request)

        if user.role == "TEACHER":
            test_category = TestCategory.objects.get(id=request.data["category"])
            test = Test.objects.create(
                question=request.data["question"],
                a=request.data["a"],
                b=request.data["b"],
                c=request.data["c"],
                d=request.data["d"],
                answer=request.data["answer"],
                level=request.data["level"],
                category=test_category,
                teacher=user.teacher_profile,
            )

            serializer = TestSerializers(test)

            return Response(serializer.data, 201)


class OrderTestInfoCreateView(APIView):
    def post(self, request):
        user = authenticate(request)
        print(user)

        if user.role == "TEACHER":
            count = request.data["count"]
            level = request.data["level"]
            deadline = request.data["deadline"]
            from_id = request.data["from_id"]
            to_id = request.data["to_id"]

            tests = Test.objects.filter(
                category__lte=to_id,
                category__gte=from_id,
                level=level,
                teacher=user.teacher_profile,
            ).order_by("id")

            order_test_info = OrderTestInfo.objects.create(
                count=count,
                level=level,
                deadline=deadline,
                from_id=from_id,
                to_id=to_id,
                teacher=user.teacher_profile,
            )

            first_id = tests.first()
            last_id = tests.last()
            random_nums_list = random.sample(
                range(int(first_id.id), int(last_id.id)), count
            )
            order_test_pack_list = list()
            for x in random_nums_list:
                order_test_pack = OrderTestPack.objects.create(
                    test=tests.get(id=x),
                    order_test_info=order_test_info,
                    teacher=user.teacher_profile,
                )
                order_test_pack_list.append(order_test_pack)
            order_test_pack_serializer = OrderTestPackSerializers(
                order_test_pack_list, many=True
            )

            return Response(order_test_pack_serializer.data, 200)


class OrderTestInfoStudentAssignView(APIView):
    def post(self, request):
        user = authenticate(request)
        if user.role == "TEACHER":
            students = request.data["students"]
            test_info = request.data["test_info"]

            order_test_info = OrderTestInfo.objects.get(id=test_info)

            for x in students:
                student_profile = StudentProfile.objects.get(id=int(x["id"]))
                order_test_info_student = OrderTestInfoStudent.objects.create(
                    student=student_profile,
                    order_test_info=order_test_info,
                    teacher=user.teacher_profile,
                )
            return Response({"message:Students succesfully assigned"}, 200)


class OrderTestPackGetView(APIView):
    def get(self, request, id):
        user = authenticate(request)

        if user.role == "STUDENT":
            student = OrderTestInfoStudent.objects.get(student=user.student_profile.id)
            if student:
                tests = OrderTestPack.objects.get(
                    order_test_info=student.order_test_info
                )
                serializer = OrderTestPackResponseSerializers(tests, many=True)

                return Response(serializer.data, 200)


class OrderTestPackStudentResultView(APIView):
    def post(self, request):
        user = authenticate(request)
        if user:
            my_list = []
            for x in request.data["students"]:
                result = x["results"]
                order_test_pack = x["order_test_pack"]

                test = OrderTestPack.objects.get(id=int(order_test_pack))
                if result == test.test.answer:
                    order_test_results = OrderTestPackStudent.objects.create(
                        result=result,
                        is_correct=True,
                        order_test_pack=test,
                        teacher=user.teacher_profile,
                    )
                else:
                    order_test_results = OrderTestPackStudent.objects.create(
                        result=result,
                        is_correct=False,
                        order_test_pack=test,
                        teacher=user.teacher_profile,
                    )
                my_list.append(order_test_results)
                serializer = OrderTestPackStudentsSerializer(my_list, many=True)

            return Response(serializer.data, 200)
