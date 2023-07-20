from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from .models import WithdrowalBalance
from django.shortcuts import get_object_or_404

from .serializers import (
    TeacherRegisterSerializer,
    StudentRegisterSerializer,
    UserSerilizer,
    GroupSerializer,
    StudentProfileSerialzer,
    AttendenceSerializer,
    PaymentSerializer,
    WithdrowalBalanceSerializer,
    ExpenseSerializer,
    TeacherProfileSerializer,
)

from rest_framework import status
from .models import User, Group, StudentProfile, TeacherProfile
import datetime
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import generics
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
import jwt


@csrf_exempt
def authenticate(request):
    # token=request.COOKIES.get('jwt')

    token = request.headers.get("jwt")

    if not token:
        raise AuthenticationFailed("Unauthenticated without token")

    try:
        payload = jwt.decode(token, "secret", algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed("Unauthenticated")

    user = User.objects.filter(id=payload["id"]).first()

    user_serialzed = UserSerilizer(user)

    if user:
        return user
    return False


class UserLoginView(APIView):
    def post(self, request):
        phone_number = request.data["phone_number"]
        password = request.data["password"]
        user = User.objects.filter(phone_number=phone_number).first()

        if user is None:
            raise AuthenticationFailed("user not found")

        if not user.check_password(password):
            raise AuthenticationFailed("incorrect password")
        payload = {
            "id": user.id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=200),
            "iat": datetime.datetime.utcnow(),
        }

        token = jwt.encode(payload, "secret", algorithm="HS256")
        response = Response()

        response.data = {"jwt": token, "role": user.role}

        return response


class UserRegisterView(APIView):
    def post(self, request):
        serializer = UserSerilizer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        return Response(serializer.data, 201)


class StudentRegisterView(APIView):
    def post(self, request):
        user = authenticate(request)

        if user:
            serializer = StudentRegisterSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            serializer.save()

            serializer_id = serializer.data["id"]

            student_ = get_object_or_404(User, id=int(serializer_id))
            student_profile = StudentProfile.objects.get(
                id=int(student_.student_profile.id)
            )
            print(user.teacher_profile.id)
            teacher_profile = TeacherProfile.objects.get(
                id=int(user.teacher_profile.id)
            )
            student_profile.teacher = teacher_profile

            student_profile.save()

            mydata = serializer.data
            mydata["id"] = student_profile.id

            return Response(mydata, 201)


class StudentLoginView(APIView):
    def post(self, request):
        phone_number = request.data["phone_number"]
        password = request.data["password"]
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


class StudentProfileList(generics.ListAPIView):
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerialzer

    def list(self, request, *args, **kwargs):
        user = authenticate(request)
        if user:
            queryset = self.filter_queryset(self.get_queryset())
            queryset = queryset.filter(teacher__id=int(user.teacher_profile.id))

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            my_dict = serializer.data
            count = 0
            for x in serializer.data:
                student = User.objects.get(student_profile=int(x["id"]))
                my_dict[count]["phone_number"] = student.phone_number
                my_dict[count]["first_name"] = student.first_name
                my_dict[count]["last_name"] = student.last_name
                count = count + 1

            return Response(my_dict, 200)


class StudentGetMe(APIView):
    def get(self, request):
        user = authenticate(request)

        if user.role == "STUDENT":
            print(user.id)
            student_profile = StudentProfile.objects.get(user__id=user.id)
            serialized_student = StudentProfileSerialzer(student_profile)

        return Response(serialized_student.data, 200)


class StudentProfileRUDView(generics.RetrieveUpdateDestroyAPIView):
    queryset = StudentProfile.objects.all()

    serializer_class = StudentProfileSerialzer
    lookup_field = "pk"

    def retrieve(self, request, *args, **kwargs):
        user = authenticate(request)

        if user:
            if user.role == "TEACHER":
                student = StudentProfile.objects.get(id=int(kwargs["pk"]))

                if student.teacher.id == user.teacher_profile.id:
                    instance = self.get_object()

                    serializer = self.get_serializer(instance)
                    return Response(serializer.data)

            else:
                student_profile = StudentProfile.objects.get(user__id=int(user.id))

                if int(student_profile.id) == int(kwargs["pk"]):
                    instance = self.get_object()

                    serializer = self.get_serializer(instance)
                    return Response(serializer.data)

            return Response(
                "You are trying to access someone's profile ",
                status=status.HTTP_403_FORBIDDEN,
            )

    def update(self, request, *args, **kwargs):
        user = authenticate(request)

        if user.role == "TEACHER":
            student = StudentProfile.objects.get(id=int(kwargs["pk"]))

            if student.teacher.id == user.teacher_profile.id:
                my_user = User.objects.get(student_profile=student.id)
                if (
                    User.objects.exclude(pk=user.id)
                    .filter(phone_number=kwargs["phone_number"])
                    .exists()
                ):
                    raise serializers.ValidationError(
                        {"email": "This email is already in use."}
                    )
                my_user.phone_number = kwargs["phone_number"]
                my_user.last_name = kwargs["last_name"]
                my_user.first_name = kwargs["first_name"]
                my_user.save()
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

                return Response(serializer.data, 200)

    def delete(self, request, *args, **kwargs):
        user = authenticate(request=request)
        if user.role == "TEACHER":
            student = StudentProfile.objects.get(id=int(kwargs["pk"]))

            if student.teacher.id == user.teacher_profile.id:
                student_to_be_deleted = User.objects.get(id=int(student.user.id))
                student_to_be_deleted.delete()
                instance = self.get_object()
                self.perform_destroy(instance)

                return Response({"message": "Object deleted successfully."}, 201)
            return Response(
                "you are trying to delete someone's profile",
                status=status.HTTP_403_FORBIDDEN,
            )


import json


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

            student = StudentProfile.objects.get(id=int(id))

            if student.teacher.id == user.teacher_profile.id:
                my_user = User.objects.get(student_profile=student.id)
                if (
                    User.objects.exclude(pk=user.id)
                    .filter(phone_number=phone_number)
                    .exists()
                ):
                    raise serializers.ValidationError(
                        {"email": "This email is already in use."}
                    )

                my_user.phone_number = phone_number
                my_user.last_name = last_name
                my_user.first_name = first_name
                my_user.save()

                student.teleg_account = teleg_account
                student.parent_phone = parent_phone
                student.parent_teleg_account = parent_teleg_account
                student.tuition_fee = tutition_fee
                student.save()

                return Response(request.data)


class AssignStudentToTeacherView(APIView):
    def put(self, request):
        user = authenticate(request)
        if user:
            student_id = int(request.data["student_id"])
            student = StudentProfile.objects.filter(id=student_id).first()
            id = int(user.id)

            teacher_id = TeacherProfile.objects.get(user__id=id)
            teacher_obj = TeacherProfile.objects.filter(id=int(teacher_id.id)).first()
            student.teacher = teacher_obj
            student.save()
            serialzer_student = StudentProfileSerialzer(student)
            return Response(serialzer_student.data, 200)


class AssignStudentToGroupView(APIView):
    def put(self, request, id):
        user = authenticate(request)
        if user:
            student_id = request.data["student_id"]
            student = StudentProfile.objects.filter(id=student_id).first()

            group_obj = Group.objects.filter(id=id).first()
            student.group = group_obj
            student.save()
            serialzer_student = StudentProfileSerialzer(student)
            return Response(serialzer_student.data, 200)


class AttendenceView(APIView):
    def post(self, request):
        request = request.data["attendence"]

        serializer = AttendenceSerializer(data=request, many=True)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        for x in request:
            student = StudentProfile.objects.filter(id=int(x["student"])).first()
            student.balance = float(student.balance) - float(student.tuitionFee)
            student.save()
            print(x["student"])

        return Response(serializer.data, 201)


class TeacherRegisterView(APIView):
    def post(self, request):
        serializer = TeacherRegisterSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, 201)


class TeachertLoginView(APIView):
    def post(self, request):
        phone_number = request.data["phone_number"]
        password = request.data["password"]
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
            teacher_profile = TeacherProfile.objects.get(id=user.teacher_profile.id)
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
        if user.role == "Teacher":
            teacher_id = TeacherProfile.objects.get(user__id=int(user.id))
            groups = Group.objects.filter(id=id, teacher__id=teacher_id).first()
            serializer = GroupSerializer(groups)
            return Response(serializer.data, 200)

    def post(self, request):
        user = authenticate(request=request)

        if str(user.role) == "TEACHER":
            name = request.data["name"]

            teacher_id = user.id
            techr_obj = TeacherProfile.objects.filter(id=teacher_id).first()
            groups = Group.objects.create(name=name, teacher=techr_obj)

            serializer = GroupSerializer(groups)
            return Response(serializer.data, 201)


class PaymentView(APIView):
    def post(self, request):
        student = StudentProfile.objects.filter(id=int(request.data["student"])).first()
        student.balance = float(student.balance) + float(request.data["sum"])
        student.save()
        serializer = PaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, 201)


class ExpenseView(APIView):
    def post(self, request):
        serializer = ExpenseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, 201)
