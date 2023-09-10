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
    OrderTestInfoAssignStudent,
    
)
import random
from .paginations import CustomPagination

from user.serializers import UserSerilizer
from .serializers import (
    TestCategorySerializer,
    TestSerializers,
    TestUpdateSerializer,
    OrderTestPackSerializers,
    OrderTestPackResponseSerializers,
    OrderTestPackStudentsSerializer,
    OrderTestPackGetSerializer,
    OrderTestInfoSerializer,
    OrderTestPackSimpleSerializers,
    TestSerializersForTeacherWithAnswer,
    OrderTestInfoAssignedStudentSerializer,
    UserForOrderTestInfoSerializer,
    
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
        my_list=[]
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

            if not tests:
               
                return Response({"message":"You dont have enough tests in choosen categories or in the chosen level"},404)
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

            try:
                order_test_info = OrderTestInfo.objects.filter(id=test_info,teacher=user.teacher_profile).first()
            except:
                return Response({"message":"There are no test_info  with this teacher"},401)

            for x in students:
                try:
                    student_profile = StudentProfile.objects.get(id=int(x["id"],teacher=user.teacher_profile))

                except:
                    return Response({"message":"Teacher does not have these students"},401)

                if OrderTestInfoAssignStudent.objects.filter(
                    student=student_profile,
                    order_test_info=order_test_info,
                    teacher=user.teacher_profile,
                ).exists():
                    raise serializers.ValidationError(
                        {
                            "message": "You have already assigned this user into this tests' info "
                        }
                    )

                order_test_info_student = OrderTestInfoAssignStudent.objects.create(
                    student_id=x,
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
                        order_test_info=test.order_test_info,
                    
                        teacher=user.teacher_profile,
                        
                    )
                else:
                    order_test_results = OrderTestPackResultsOfStudent.objects.create(
                        result=result,
                        is_correct=False,
                        student=student,
                        order_test_pack=test,
                        order_test_info=test.order_test_info,
                        teacher=user.teacher_profile,
                    )
                my_list.append(order_test_results)
            serializer = OrderTestPackStudentsSerializer(my_list, many=True)

            return Response(serializer.data, 200)


class OrderTestInfoListView(generics.ListAPIView):
    queryset = OrderTestInfo.objects.all()
    pagination_class = CustomPagination
    serializer_class = OrderTestInfoSerializer

    def list(self, request, *args, **kwargs):
        user = authenticate(request)
        if user.role=="TEACHER":
            queryset = self.filter_queryset(self.get_queryset())
            queryset = queryset.filter(teacher=user.teacher_profile)
            page = self.paginate_queryset(queryset)
            my_data = []
            for x in queryset:
                orders = OrderTestInfoAssignStudent.objects.filter(
                    order_test_info=x
                ).count()

                if page is not None:
                    
                    serializer = OrderTestInfoSerializer(x)
                    smth = serializer.data
                    smth["student_count"] = orders

                    my_data.append(smth)
                    
            return self.get_paginated_response(my_data)

class OrderTestInfoGetTeacherView(APIView):
    def get(self,request):
        user=authenticate(request)
        my_list=[]
        if user:
            order_test_info_id=request.query_params["id"]
            try:
                order_test_info_assigned_students=OrderTestInfoAssignStudent.objects.filter(order_test_info=order_test_info_id)
                if order_test_info_assigned_students:
                    number_of_assigned_students=order_test_info_assigned_students.count()

                    order_test_info=OrderTestInfo.objects.get(id=order_test_info_id,teacher=user.teacher_profile)
                    for x in order_test_info_assigned_students:
                        students=User.objects.filter(student_profile=x.student)
                        student_serializer=UserForOrderTestInfoSerializer(students,many=True)
                        serializer=OrderTestInfoSerializer(order_test_info) 
                        my_data=serializer.data
                        my_list.append(student_serializer.data)
                    my_data["students"]=my_list
                    my_data["student_count"]=number_of_assigned_students
                    return Response(my_data,200)
                else:
                    order_test_info=OrderTestInfo.objects.get(id=order_test_info_id,teacher=user.teacher_profile)
                    serializer=OrderTestInfoSerializer(order_test_info)
                    my_data=serializer.data
                    my_data["students"]=None
                    my_data["student_count"]=0
                    return Response(my_data,200)

            except Exception as e:
                print(e)
                return Response({"message":"Error happened in getting student list or in  order test"})


            

class GetTeacherTestInfoStudentResultsView(APIView):
    def get(self,request):
        user=authenticate(request)
        student_id=request.query_params["student_id"]
        order_test_info_id=request.query_params["test_info_id"]

        order_test_info_assigned_student_result=OrderTestInfoAssignStudent.objects.filter(student_id=student_id,order_test_info__id=order_test_info_id,teacher=user.teacher_profile)
        serializer=OrderTestInfoAssignedStudentSerializer(order_test_info_assigned_student_result,many=True)
        
        return Response(serializer.data,201)
     











class GetOrderTestInfoTestPackView(generics.ListAPIView):
    queryset = OrderTestPack.objects.all()
    serializer_class = OrderTestPackSerializers
    pagination_class = CustomPagination

    def list(self, request, *args, **kwargs):
        user = authenticate(request)
        if user:
            id = kwargs["id"]
            try:
                queryset = self.filter_queryset(self.get_queryset())

                order_test_info = OrderTestInfo.objects.get(id=id)

                queryset = queryset.filter(
                    teacher=user.teacher_profile, order_test_info=order_test_info
                )
                if not queryset:
                    return Response({"message":"there is no test in this test_info"},200)

                page = self.paginate_queryset(queryset)

                if page is not None:
                    serializer = self.get_serializer(page, many=True)

                    return self.get_paginated_response(serializer.data)
            except Exception as e:
                print(e)
                return Response({"message":"Error happened in test_info"},400)


class OrderTestinfoAssignedStudentsView(APIView):
    def get(self,request):
        user=authenticate(request)
        if user:
           
                assigned_student=OrderTestInfoAssignStudent.objects.get(student=user.student_profile)
            
                print(assigned_student)

                if assigned_student:
                

                    serializer=OrderTestInfoAssignedStudentSerializer(assigned_student,many=True)


                    return Response(serializer.data,200)
                
                return Response({"error":"Object Not Found"},404)




class TotalTestCountView(APIView):
    def get(self,request):
        user=authenticate(request)
        if user.role=="TEACHER":
            test=Test.objects.filter(teacher=user.teacher_profile).count()
            return Response(test,200)
        return Response({"error":"Forbidden"},404)
    

##############################

class TestInfoDetailForStudentView(APIView):
    def get(self,request,id):
        user=authenticate(request=request)
        if user.role=="STUDENT":
           
            try:

                order_test_info=OrderTestInfoAssignStudent.objects.get(order_test_info__id=id,student=user.student_profile)
              
                """ print("smth")
                print(user.student_profile)
                if user.student_profile.teacher!=order_test_info.teacher:
                    return Response({"message":"you are not this teacher's student , bula siz bashqa odamni uquvchisikankisiz ,nima qlasz berlaga adashib"},401)"""
            except:

                return Response({"message":"you are not assigned or there is not test info"},401)
        
            my_dict={}
            if order_test_info.submitted==False:

                print("heree")
                

                serializer=OrderTestInfoAssignedStudentSerializer(order_test_info)
                if serializer.is_valid():
                    print(serializer.data)

                    test_pack=OrderTestPack.objects.filter(order_test_info=order_test_info.order_test_info)

                    test_pack_serializer=OrderTestPackSerializers(test_pack,many=True)
                
                    my_dict=serializer.data
                    my_dict["test_pack"]=test_pack_serializer.data
                
                
                    return Response(my_dict,200)
            
        return Response({"message":"Unauthorized"},401)
            
            
            


