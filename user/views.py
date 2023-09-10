from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from django.db import connection



from .paginations import CustomPagination
from django.shortcuts import get_object_or_404
from finance.serializers import ExpenseSerializer,PaymentSerializer

from .serializers import (
    TeacherGetMeSerailizer,
    TeacherRegisterSerializer,
    StudentRegisterSerializer,
    UserSerilizer,
    GroupSerializer,
    StudentProfileSerialzer,
    AttendenceSerializer,
    
    WithdrowalBalanceSerializer,
    
    TeacherProfileSerializer,
    StudentFilterListViewSerializer,
    StudentIncomeSerializer,
    StudentGetMeSerializer,
)
from .utils import send_to_telegram
from rest_framework import status
from .models import User, Group, StudentProfile, TeacherProfile, UserTraffic, Config
import datetime
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import generics
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
import jwt
import logging

from django.db import reset_queries

def database_debug(func):
    def inner_func(*args, **kwargs):
        reset_queries()
        results = func(*args, **kwargs)
        query_info = connection.queries
        print('function_name: {}'.format(func.__name__))
        print('query_count: {}'.format(len(query_info)))
        queries = ['{}\n\n'.format(query['sql']) for query in query_info]
        print('queries: \n{}\n'.format(''.join(queries)))

        return results
    return inner_func


@csrf_exempt

def authenticate(request):
    # token=request.COOKIES.get('jwt')

    token = request.headers.get("jwt")

    if not token:
        raise AuthenticationFailed("Unauthenticated without token")

    try:
        payload = jwt.decode(token, "secret", algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed({"message":"Unauthenticated"})
    except:
        raise AuthenticationFailed({"message":"Token Not Provided"})

    user = User.objects.get(id=payload["id"])

    if user:
        return user
    return False


class UserLoginView(APIView):
    def post(self, request):
        try:
            phone_number = request.data["phone_number"]
            password = request.data["password"]
        except KeyError:
         
            return Response({"message":"phone_number or password not provided correctly"},400)
        
        user = User.objects.filter(phone_number=phone_number).first()

        if user is None:
            raise AuthenticationFailed("user not found")

        if not user.check_password(password):
            raise AuthenticationFailed("incorrect password")
        payload = {
            "id": user.id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=2),
            "iat": datetime.datetime.utcnow(),
        }

        token = jwt.encode(payload, "secret", algorithm="HS256")
        response = Response()

        response.data = {"jwt": token, "role": user.role}

        return response


class UserRegisterView(APIView):
    def post(self, request):
        try:

            serializer = UserSerilizer(data=request.data)
            serializer.is_valid(raise_exception=True)

            serializer.save()
        except:
            logging.info("error happened because of problem in user serialization ")
            return Response({"message":"Error happened while creating user"})
        return Response(serializer.data, 201)



class StudentRegisterView(APIView):
    @database_debug
    def post(self, request):
        user = authenticate(request)
        # print(len(connection.queries),"authenticate")    
        print(len(connection.queries),"end of fields")
        if user:
            try:
                print(user.teacher_profile)
                print(len(connection.queries),"in try")

                config_data = Config.objects.get(teacher=user.teacher_profile)
                # config_data = Config.objects.select_related('teacher').get(teacher=user.teacher_profile)
                print(len(connection.queries),"87134682736rhdwieufih")
            except Exception as e:
                logging.error(e)
                return Response({"message":"You should first create tutition fee for your course then you can create student "},400)
            print(len(connection.queries),"config data")
            request.data["student_profile"]["tuition_fee"] = config_data.tuition_fee
            print(len(connection.queries),"config daata ")
            try:
                print(request.data["phone_number"])
                registered_student=User.objects.filter(phone_number=request.data["phone_number"],role="STUDENT").first()
                if registered_student:
                    return Response({"message":"User with this phone number already registered"},400)
            except:
                return Response({"message":"please fill all fields"},400)
            try:
                serializer = StudentRegisterSerializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
            except Exception as e:
                print(e)
                return Response({"message":"fill all fields"},400)
                       
            serializer_id = serializer.data["id"]

            student_ = get_object_or_404(User, id=int(serializer_id))
            
            try:

                student_profile = StudentProfile.objects.get(
                    id=int(student_.student_profile.id)
                )
            except:
                return Response({"message":"Not Found StudentProfile"})
            try:

                teacher_profile = TeacherProfile.objects.get(
                    id=int(user.teacher_profile.id)
                )
            
                student_profile.teacher = teacher_profile
                student_profile.save()
            except Exception as e:
                print(e)
                return Response({"message":"Techer not found and problem finding student"})
            
            try:
                user_income = UserTraffic.objects.get(teacher=teacher_profile)

                if serializer.data["student_profile"]["source"] == "INSTAGRAM":
                    user_income.instagram = int(user_income.instagram) + 1
                elif serializer.data["student_profile"]["source"] == "FACEBOOK":
                    user_income.facebook = user_income.facebook + 1
                elif serializer.data["student_profile"]["source"] == "TELEGRAM":
                    user_income.telegram = user_income.telegram + 1
                elif serializer.data["student_profile"]["source"] == "LEAFLET":
                    user_income.leaflet = user_income.leaflet + 1
                elif serializer.data["student_profile"]["source"] == "OTHER":
                    user_income.other = user_income.other + 1
                elif serializer.data["student_profile"]["source"] == "FRIEND":
                    user_income.friend = user_income.friend + 1
                user_income.save()

                mydata = serializer.data
                mydata["id"] = student_profile.id

                print(len(connection.queries),"87134682736rhdwieufih")
                return Response(mydata, 201)
            except Exception as e:
                print(e)
                return Response({"message":"User Traffic not Found"})


class StudentLoginView(APIView):
    def post(self, request):
        try:
            phone_number = request.data["phone_number"]
            password = request.data["password"]
        except:
            return Response({"message":"not all user provided"},400)
        
        student = User.objects.filter(phone_number=phone_number).first()

        if student is None:
            raise AuthenticationFailed("user not found")

        if not student.check_password(password):
            raise AuthenticationFailed("incorrect password")

        payload = {
            "id": student.id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=200),
            "iat": datetime.datetime.utcnow(),
        }

        token = jwt.encode(payload, "secret", algorithm="HS256")
        response = Response()
        response.status_code = 200

        response.data = {"jwt": token, "role": student.role}

        return response


class StudentProfileListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = StudentFilterListViewSerializer
    pagination_class = CustomPagination

    def list(self, request, *args, **kwargs):
        user = authenticate(request)
        if user:
            
          

            phone_number = request.query_params.get("phone_number", None)

            first_name = request.query_params.get("first_name", None)
            last_name = request.query_params.get("last_name", None)
            group = request.query_params.get("group", None)
            deptor = request.query_params.get("deptor", None)
            
            try:

                queryset = self.filter_queryset(self.get_queryset())
                queryset = queryset.filter(student_profile__teacher=user.teacher_profile)
            except Exception as e:
                print(e)
                return Response({"message":"Problem finding techer profile "},400)

            if phone_number != "" and phone_number is not None:
                print("phone_number")
                queryset = queryset.filter(phone_number__contains=phone_number)
            if first_name != "" and first_name is not None:
                print("first_name")
                queryset = queryset.filter(first_name__contains=first_name)
            if last_name != "" and last_name is not None:
                queryset = queryset.filter(last_name__contains=last_name)
            if group != "" and group is not None:
                queryset = queryset.filter(student_profile__group=group)
            if deptor == "True":
                print("it is true")
                queryset = queryset.filter(student_profile__balance__lt=0)
                print(queryset)
            if deptor == "False":
                print("that")
                queryset = queryset.filter(student_profile__balance__gte=0)
                print(queryset)

            # queryset = queryset.filter(teacher__id=int(user.teacher_profile.id))

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)

                return self.get_paginated_response(serializer.data)
        return Response({"message":"Not Authentcaated"},403)

class StudentFilterView(APIView):
    def get(self, request):
        user = authenticate(request=request)

        if user.role == "TEACHER":
            qs = User.objects.all()

            phone_number = request.query_params.get("phone_number", None)

            first_name = request.query_params.get("first_name", None)
            last_name = request.query_params.get("last_name", None)
            group = request.query_params.get("group", None)
            deptor = request.query_params.get("deptor", None)
            print(deptor)

            if phone_number != "" and phone_number is not None:
                qs = qs.filter(phone_number__contains=phone_number)
            elif first_name != "" and first_name is not None:
                qs = qs.filter(first_name__contains=first_name)
            elif last_name != "" and last_name is not None:
                qs = qs.filter(last_name__contains=last_name)
            elif group != "" and group is not None:
                qs = qs.filter(student_profile__group=group)
            elif deptor == True:
                print("this")
                qs = qs.filter(student_profile__balance__lt=0)
                print(qs)
            elif deptor == False:
                print("that")
                qs = qs.filter(student_profile__balance__gte=0)
                print(qs)

            serializer = UserSerilizer(qs, many=True)
            if serializer.is_valid(raise_exception=True):

                return Response(serializer.data, status=status.HTTP_200_OK)
        return status.HTTP_401_UNAUTHORIZED


class GetMeView(APIView):
    def get(self, request):
        user = authenticate(request)

        if user.role == "STUDENT":
            serializer = StudentGetMeSerializer(user)
            return Response(serializer.data, 200)

        elif user.role == "TEACHER":
            serializer = TeacherGetMeSerailizer(user)
            return Response(serializer.data, 200)
        
        return Response({"message":"User nott found"},404)


class StudentProfileRUDView(generics.RetrieveUpdateDestroyAPIView):
    queryset = StudentProfile.objects.all()

    serializer_class = StudentProfileSerialzer
    lookup_field = "pk"

    def retrieve(self, request, *args, **kwargs):
        user = authenticate(request)

        if user:
            if user.role == "TEACHER":
                try:
                    student = StudentProfile.objects.get(id=int(kwargs["pk"]))
                except:
                    return Response({"message":"Not Found"},404)

                if student.teacher.id == user.teacher_profile.id:
                    instance = self.get_object()

                    serializer = self.get_serializer(instance)
                    return Response(serializer.data)

            else:
                try:
                    student_profile = StudentProfile.objects.get(user__id=int(user.id))
                except:
                    return Response({"message":"Not Found"},404)

                if int(student_profile.id) == int(kwargs["pk"]):
                    instance = self.get_object()

                    serializer = self.get_serializer(instance)
                    return Response(serializer.data)

            return Response(
                "You are trying to access someone's profile ",
                status=status.HTTP_403_FORBIDDEN,
            )

    def delete(self, request, *args, **kwargs):
        user = authenticate(request=request)
        if user.role == "TEACHER":
            try:
                student = StudentProfile.objects.get(id=int(kwargs["pk"]))
            except:
                return Response({"message":"Not Found"},404)


            if student.teacher.id == user.teacher_profile.id:
                try:
                    student_to_be_deleted = User.objects.get(id=int(student.user.id))
                    student_to_be_deleted.delete()
                    instance = self.get_object()
                    self.perform_destroy(instance)
                except Exception as e:
                    print(e)
                    return Response({"message":"Not Found"},404)

                return Response({"message": "Object deleted successfully."}, 201)
            return Response(
                "you are trying to delete someone's profile",
                status=status.HTTP_403_FORBIDDEN,
            )


class UpdateStudentProfileView(APIView):
    def put(self, request, id):
        user = authenticate(request)
        if user.role == "TEACHER":
            phone_number = request.data["phone_number"]
            last_name = request.data["last_name"]
            first_name = request.data["first_name"]
            teleg_account = request.data["teleg_account"]
            parent_phone = request.data["parent_phone"]
            parent_teleg_account = request.data["parent_teleg_account"]
            tutition_fee = request.data["tuition_fee"]

            try:

                student = StudentProfile.objects.get(id=int(id))
            except Exception as e:
                return Response({"message":"Not Found"},404)

            if student.teacher.id == user.teacher_profile.id:
                try:
                    my_user = User.objects.get(student_profile=student)
                except:
                    return Response({"message":"Not Found"},404)
                print(my_user, "my_useeer")
                print(
                    User.objects.exclude(student_profile=student).filter(
                        phone_number=phone_number
                    )
                )
                if (
                    User.objects.exclude(student_profile=student)
                    .filter(phone_number=phone_number)
                    .exists()
                ):
                    raise serializers.ValidationError(
                        {"phone_number": "This phone_number is already in use."}
                    )
                try:
                    my_user.phone_number = phone_number
                    my_user.last_name = last_name
                    my_user.first_name = first_name
                    my_user.save()

                    student.teleg_account = teleg_account
                    student.parent_phone = parent_phone
                    student.parent_teleg_account = parent_teleg_account
                    student.tuition_fee = tutition_fee
                    student.save()
                except Exception as e:
                    print(e)
                    return Response({"message":"Not Saaved succesfully"},400)

                return Response(request.data)


class AssignStudentToTeacherView(APIView):
    def put(self, request):
        user = authenticate(request)
        if user:

            student_id = int(request.data["student_id"])
            try:
                student = StudentProfile.objects.filter(id=student_id).first()
            except Exception as e:
                print(e)
                return Response({"message":"Not Found"},404)
            id = int(user.id)
            try:
                teacher_id = TeacherProfile.objects.get(user__id=id)
                teacher_obj = TeacherProfile.objects.filter(id=int(teacher_id.id)).first()
            except Exception as e:
                print(e)
                return Response({"message":"Not found techer profile"})
            student.teacher = teacher_obj
            student.save()
            serialzer_student = StudentProfileSerialzer(student)
            return Response(serialzer_student.data, 200)


class AssignStudentToGroupView(APIView):
    def put(self, request, id):
        user = authenticate(request)
        if user.role == "TEACHER":

            student_id = request.data["student_id"]
            try:
                student = StudentProfile.objects.filter(
                    id=student_id, teacher=user.teacher_profile.id
                ).first()
            except Exception as e:
                print(e)
                return Response({"message":"Not Found Student Profile"},404)
            
            try:
                group_obj = Group.objects.filter(
                    id=id, teacher=user.teacher_profile.id
                ).first()
            except Exception as e:
                print(e)
                return Response({"message":"Not Found group"},404)
            student.group = group_obj
            student.save()
            serialzer_student = StudentProfileSerialzer(student)
            return Response(serialzer_student.data, 200)


class AttendenceView(APIView):
    def post(self, request):
        user = authenticate(request)
        if user:
            attendence = request.data["attendence"]
            try:

                serializer = AttendenceSerializer(data=attendence, many=True)

                serializer.is_valid(raise_exception=True)
                serializer.save()
            except Exception as e:
                print(e)
                return Response({"message":"Error in Attendence"})

            for x in attendence:
                try:
                    student = StudentProfile.objects.filter(id=int(x["student"])).first()

                    user = User.objects.get(student_profile=student)
                    student.balance = float(student.balance) - float(student.tuition_fee)
                except Exception as e:
                    print(e)
                    return Response({"message":"not found student"},404)
                student.save()
                try:
                    send_to_telegram(
                        chat_id=student.parent_telegram_id,
                        first_name=user.first_name,
                        last_name=user.last_name,
                        status=x["status"],
                    )
                except Exception as e:
                    print(e)
                    logging.error("not sent telegram data")
                

            return Response(serializer.data, 201)


class TeacherRegisterView(APIView):
    def post(self, request):

        serializer = TeacherRegisterSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, 201)


class TeachertLoginView(APIView):
    def post(self, request):
        try:
            phone_number = request.data["phone_number"]
            password = request.data["password"]
        except:
            return Response({"message":"password or number not provided properly"},400)
        teacher = User.objects.filter(phone_number=phone_number).first()

        if teacher is None:
            raise AuthenticationFailed("user not found")

        if not teacher.check_password(password):
            raise AuthenticationFailed("incorrect password")
        payload = {
            "id": teacher.id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=200),
            "iat": datetime.datetime.utcnow(),
        }

        token = jwt.encode(payload, "secret", algorithm="HS256")
        response = Response()

        response.data = {"jwt": token, "role": teacher.role}
        response.status_code = 200
        return response


class TeacherGetMeView(APIView):
    def get(self, request):
        user = authenticate(request)

        if user.role == "TEACHER":
            print(user.id)
            try:
                teacher_profile = TeacherProfile.objects.get(id=user.teacher_profile.id)
            except:
                pass
            serialized_teacher = TeacherProfileSerializer(teacher_profile)
            my_data = serialized_teacher.data
            my_data["first_name"] = user.first_name
            my_data["last_name"] = user.last_name
            return Response(my_data, 200)


class TeachertRUDView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TeacherProfile.objects.all()

    serializer_class = TeacherProfileSerializer
    lookup_field = "pk"

    def retrieve(self, request, *args, **kwargs):
        user = authenticate(request)
        if user.role == "TEACHER":
            if int(user.teacher_profile.id) == kwargs["pk"]:
                instance = self.get_object()
                serializer = self.get_serializer(instance)
                return Response(serializer.data)
            return Response(
                "you are trying to get non personal profile",
                status=status.HTTP_403_FORBIDDEN,
            )
        return Response("you are not teacher", status=status.HTTP_403_FORBIDDEN)

    def update(self, request, *args, **kwargs):
        user = authenticate(request)

        if user.role == "TEACHER":
            if user.id == kwargs["pk"]:
                partial = kwargs.pop("partial", False)
                instance = self.get_object()
                serializer = self.get_serializer(
                    instance, data=request.data, partial=partial
                )
                serializer.is_valid(raise_exception=True)
                self.perform_update(serializer)

                if getattr(instance, "_prefetched_objects_cache", None):
                    # If 'prefetch_related' has been applied to a queryset, we need to
                    # forcibly invalidate the prefetch cache on the instance.
                    instance._prefetched_objects_cache = {}

                return Response(serializer.data)
            return Response(
                "you are trying to update someone's profile",
                status=status.HTTP_403_FORBIDDEN,
            )
        return Response("you are not teacher", status=status.HTTP_403_FORBIDDEN)


class GroupRUDView(APIView):
    def get(self, request, id):
        user = authenticate(request=request)

        if user.role == "TEACHER":
            try:
                group = Group.objects.get(id=id, teacher=user.teacher_profile.id)
                group_count = StudentProfile.objects.filter(group=group).count()

                serializer = GroupSerializer(group)
                data_ser = serializer.data
                data_ser["student_number"] = group_count
                print(data_ser["date"])

                data_ser["days"] = data_ser["days"].split(",")

                data_ser["date"] = data_ser["date"].split(",")
                return Response(data_ser, 200)
            except Exception as e:

                print(e)
                return Response(
                    {"message": "dont try to connects other's profile"}, 401
                )

    def post(self, request):
        user = authenticate(request=request)

        if str(user.role) == "TEACHER":
            name = request.data["name"]
            days = request.data["days"]
            date = request.data["date"]
            my_days = ""
            for x in days:
                my_days = my_days + x + ","
            my_days = my_days[:-1]
            my_date = ""
            for y in date:
                my_date = my_date + y + ","
            my_date = my_date[:-1]
            groups = Group.objects.create(
                name=name, days=my_days, date=my_date, teacher=user.teacher_profile
            )

            serializer = GroupSerializer(groups)
            return Response(serializer.data, 201)

    def put(self, request, id):
        user = authenticate(request)
        if user.role == "TEACHER":
            name = request.data["name"]
            days = request.data["days"]
            date = request.data["date"]
            my_days = ""
            for x in days:
                my_days = my_days + x + ","
            my_days = my_days[:-1]
            my_date = ""
            for y in date:
                my_date = my_date + y + ","
            my_date = my_date[:-1]

            group = Group.objects.get(id=id, teacher=user.teacher_profile.id)
            group.name = name
            group.days = my_days
            group.date = my_date

            group.save()

    def delete(self, request, id):
        user = authenticate(request=request)
        if str(user.role) == "TEACHER":
            group = Group.objects.get(id=id, teacher=user.teacher_profile.id)
            group.delete()

            return Response({"messege": "object deleted succesfully"}, 200)


class GroupList(APIView):
    def get(self, request):
        user = authenticate(request)
        if user.role == "TEACHER":
            groups = Group.objects.filter(teacher=user.teacher_profile.id)

            serializer = GroupSerializer(groups, many=True)
            my_serializer = serializer.data
            my_list = list()
            for x in my_serializer:
                group = groups.get(id=x["id"])
                group_count = StudentProfile.objects.filter(group=group).count()

                x["student_number"] = group_count
                my_list.append(x)

            return Response(my_list, 200)


class GroupStudentListView(APIView):
    def get(self, request, id):
        user = authenticate(request)
        if user.role == "TEACHER":
            group = Group.objects.get(id=id, teacher=user.teacher_profile)
            students = StudentProfile.objects.filter(
                group=group, teacher=user.teacher_profile.id
            )

            my_data = []
            serializer = StudentProfileSerialzer(students, many=True)
            my_data = serializer.data
            count = 0
            for x in students:
                user = User.objects.get(student_profile=x)
                my_data[0]["phone_number"] = user.phone_number
                my_data[count]["first_name"] = user.first_name
                my_data[count]["last_name"] = user.last_name

                count = count + 1

            return Response(serializer.data, 200)


class PaymentView(APIView):
    def post(self, request):
        user = authenticate(request)
        if user:
            student = StudentProfile.objects.get(
                id=int(request.data["student"])
            )
            student.balance = float(student.balance) + float(request.data["sum"])
            student.save()
            request.data["teacher"] = user.teacher_profile.id
            serializer = PaymentSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, 201)


class ExpenseView(APIView):
    def post(self, request):
        user = authenticate(request)
        if user:
            serializer = ExpenseSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, 201)


class UserTrafficView(APIView):
    def get(self, request):
        user = authenticate(request)
        if user:
            income_sources = UserTraffic.objects.get(teacher=user.teacher_profile)
            serializer = StudentIncomeSerializer(income_sources)
            return Response(serializer.data, 201)
