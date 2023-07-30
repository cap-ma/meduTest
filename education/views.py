from django.shortcuts import render
from rest_framework.response import Response
from user.models import TeacherProfile, StudentProfile, User
from user.views import authenticate
from .utils import sched, send_test_results_to_parent
from datetime import date, datetime
from rest_framework import status
from .models import (
    Test,
    TestCategory,
    OrderTestInfo,
    OrderTestInfoAssignStudent,
    OrderTestPack,
    OrderTestPackResultsOfStudent,
)
import random
from .paginations import CustomPagination

from .serializers import (
    TestCategorySerializer,
    TestSerializers,
    TestUpdateSerializer,
    OrderTestPackSerializers,
    OrderTestPackResponseSerializers,
    OrderTestPackStudentsSerializer,
    OrderTestPackGetSerializer,
    OrderTestInfoSerializers,
    OrderTestPackSimpleSerializers,
    TestSerializersForTeacherWithAnswer,
)

from rest_framework import generics, serializers
from rest_framework.views import APIView
from django.utils import timezone


class TestPackView(APIView):
    def get(self, request):
        pass


class TestUDView(APIView):
    def put(self, request, pk):
        user = authenticate(request)
        if user.role == "TEACHER":
            try:
                instance = Test.objects.get(pk=pk, teacher=user.teacher_profile)
            except Test.DoesNotExist:
                return Response({"error": "Object not found."}, 404)

            serializer = TestUpdateSerializer(instance, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, 400)

    def delete(self, request, pk):
        user = authenticate(request)
        if user.role == "TEACHER":
            try:
                instance = Test.objects.get(pk=pk, teacher=user.teacher_profile)
            except Test.DoesNotExist:
                return Response({"error": "Object not found."}, 404)

            instance.delete()
            return Response(
                {"message": "Muvaffaqqiyatli o'chirildi"},
                status=status.HTTP_204_NO_CONTENT,
            )


class TestListViewForTeacher(generics.ListAPIView):
    queryset = Test.objects.all()
    pagination_class = CustomPagination
    serializer_class = TestSerializersForTeacherWithAnswer

    def list(self, request, *args, **kwargs):
        user = authenticate(request)
        if user.role == "TEACHER":
            queryset = self.filter_queryset(self.get_queryset())
            queryset = queryset.filter(teacher=user.teacher_profile).order_by("id")

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)


class TestListView(generics.ListAPIView):
    queryset = Test.objects.all()
    pagination_class = CustomPagination
    serializer_class = TestSerializers

    def list(self, request, *args, **kwargs):
        user = authenticate(request)
        if user.role == "TEACHER":
            queryset = self.filter_queryset(self.get_queryset())
            queryset = queryset.filter(teacher=user.teacher_profile).order_by("id")

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)


class TestCategoryListView(generics.ListAPIView):
    queryset = TestCategory.objects.all()
    pagination_class = CustomPagination
    serializer_class = TestCategorySerializer

    def list(self, request, *args, **kwargs):
        user = authenticate(request)
        if user.role == "TEACHER":
            queryset = self.filter_queryset(self.get_queryset())
            queryset = queryset.filter(teacher=user.teacher_profile)

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                print("zxvczxfv")
                print(serializer.data)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            print(serializer.data)
            print("zxvczxfv")
            return Response(serializer.data)


class TestCategoryUDView(APIView):
    def put(self, request, pk):
        user = authenticate(request)
        if user.role == "TEACHER":
            try:
                instance = TestCategory.objects.get(pk=pk, teacher=user.teacher_profile)
            except TestCategory.DoesNotExist:
                return Response({"error": "Object not found."}, 404)

            serializer = TestCategorySerializer(instance, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, 400)

    def delete(self, request, pk):
        user = authenticate(request)
        if user.role == "TEACHER":
            try:
                instance = TestCategory.objects.get(pk=pk, teacher=user.teacher_profile)
            except TestCategory.DoesNotExist:
                return Response({"error": "Object not found."}, 404)

            instance.delete()
            return Response(
                {"message": "Muvaffaqqiyatli o'chirildi"},
                status=status.HTTP_204_NO_CONTENT,
            )


class TestGetCategoryById(APIView):
    def get(self, request, id):
        user = authenticate(request)
        if user.role == "TEACHER":
            test_category = TestCategory.objects.get(
                id=id, teacher=user.teacher_profile
            )
            serializer = TestCategorySerializer(test_category)
            return Response(serializer.data, 200)


class TestGetCategory(generics.ListAPIView):
    queryset = Test.objects.all()
    pagination_class = CustomPagination
    serializer_class = TestSerializers

    def list(self, request, *args, **kwargs):
        user = authenticate(request)
        if user.role == "TEACHER":
            print(kwargs, "kwargs")
            category = request.query_params.get("category", None)
            level = request.query_params.get("level", None)

            queryset = self.filter_queryset(self.get_queryset())
            queryset = queryset.filter(teacher=user.teacher_profile).order_by("id")
            if category != "" and category is not None:
                queryset = queryset.filter(category__id=category)
            elif level != "" and level is not None:
                queryset = queryset.filter(level=level)

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)


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
            test_category = TestCategory.objects.get(
                id=request.data["category"], teacher=user.teacher_profile
            )
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

        if user.role == "TEACHER":
            count = request.data["count"]
            level = request.data["level"]
            deadline = request.data["deadline"]
            categories = request.data["categories"]
            int_categories = [int(x) for x in categories]

            tests = Test.objects.filter(
                category__in=int_categories,
                level=level,
                teacher=user.teacher_profile,
            ).order_by("id")
            print(tests, "adfadgadf")

            order_test_info = OrderTestInfo.objects.create(
                count=count,
                level=level,
                deadline=deadline,
                categories=categories,
                teacher=user.teacher_profile,
            )

            deadline_for_scheduled_task = deadline.split("-")

            sched.add_job(
                send_test_results_to_parent,
                "date",
                run_date=datetime(
                    int(deadline_for_scheduled_task[0]),
                    int(deadline_for_scheduled_task[1]),
                    int(deadline_for_scheduled_task[2]),
                    17,
                    45,
                    0,
                ),
                args=[order_test_info.id],
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
            serialzer = OrderTestPackSimpleSerializers(order_test_pack)
            my_list = serialzer.data
            my_list["name"] = "Test"

            """my_list = order_test_pack
            my_list["name"] = "Tests"""
            order_test_pack_serializer = OrderTestPackSerializers(
                order_test_pack_list, many=True
            )

            return Response(my_list, 200)


class OrderTestInfoStudentAssignView(APIView):
    def post(self, request):
        user = authenticate(request)
        if user.role == "TEACHER":
            students = request.data["students"]
            test_info = request.data["test_info"]

            order_test_info = OrderTestInfo.objects.get(id=test_info)

            for x in students:
                student_profile = StudentProfile.objects.get(id=int(x["id"]))

                if OrderTestInfoAssignStudent.objects.filter(
                    student=student_profile,
                    order_test_info=order_test_info,
                    teacher=user.teacher_profile,
                ).exists():
                    raise serializers.ValidationError(
                        {
                            "message": "You have assigned this user into this tests' pack "
                        }
                    )

                order_test_info_student = OrderTestInfoAssignStudent.objects.create(
                    student=student_profile,
                    order_test_info=order_test_info,
                    teacher=user.teacher_profile,
                )
            return Response({"message:Students succesfully assigned"}, 200)


class OrderTestPackListView(generics.ListAPIView):
    queryset = OrderTestPack.objects.all()
    pagination_class = CustomPagination
    serializer_class = OrderTestPackGetSerializer

    def list(self, request, *args, **kwargs):
        user = authenticate(request)
        if user.role == "TEACHER":
            queryset = self.filter_queryset(self.get_queryset())
            queryset = queryset.filter(teacher=user.teacher_profile).order_by(
                "-created_at"
            )

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)


class OrderTestPackGetView(APIView):
    def get(self, request, id):
        user = authenticate(request)

        if user.role == "STUDENT":
            student = OrderTestInfoAssignStudent.objects.get(
                student=user.student_profile.id
            )
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
                student_data = x["student"]

                test = OrderTestPack.objects.get(id=int(order_test_pack))
                print(student_data, "student_id")
                print(test.order_test_info, "order_Test_info")
                print(user.teacher_profile, "teacher_profile")

                student = OrderTestInfoAssignStudent.objects.get(
                    student__id=student_data,
                    submitted=False,
                    teacher=user.teacher_profile,
                    order_test_info=test.order_test_info,
                )
                print(student, "this is a student")
                if str(result) == str(test.test.answer):
                    order_test_results = OrderTestPackResultsOfStudent.objects.create(
                        result=result,
                        student=student,
                        is_correct=True,
                        order_test_pack=test,
                        teacher=user.teacher_profile,
                    )
                else:
                    order_test_results = OrderTestPackResultsOfStudent.objects.create(
                        result=result,
                        is_correct=False,
                        student=student,
                        order_test_pack=test,
                        teacher=user.teacher_profile,
                    )
                my_list.append(order_test_results)
            serializer = OrderTestPackStudentsSerializer(my_list, many=True)

            return Response(serializer.data, 200)


class OrderTestInfoView(generics.ListAPIView):
    queryset = OrderTestInfo.objects.all()
    pagination_class = CustomPagination
    serializer_class = OrderTestInfoSerializers

    def list(self, request, *args, **kwargs):
        user = authenticate(request)
        if user:
            queryset = self.filter_queryset(self.get_queryset())
            queryset = queryset.filter(teacher=user.teacher_profile)
            page = self.paginate_queryset(queryset)
            my_data = []
            for x in queryset:
                orders = OrderTestInfoAssignStudent.objects.filter(
                    order_test_info=x
                ).count()

                if page is not None:
                    serializer = OrderTestInfoSerializers(x)
                    smth = serializer.data
                    smth["student_count"] = orders

                    my_data.append(smth)
            return self.get_paginated_response(my_data)


class GetOrderTestInfoTestPackView(generics.ListAPIView):
    queryset = OrderTestPack.objects.all()
    serializer_class = OrderTestPackSerializers
    pagination_class = CustomPagination

    def list(self, request, *args, **kwargs):
        user = authenticate(request)
        if user:
            id = kwargs["id"]
            queryset = self.filter_queryset(self.get_queryset())
            order_test_info = OrderTestInfo.objects.get(id=id)
            queryset = queryset.filter(
                teacher=user.teacher_profile, order_test_info=order_test_info
            )
            page = self.paginate_queryset(queryset)

            if page is not None:
                serializer = self.get_serializer(page, many=True)

                return self.get_paginated_response(serializer.data)
