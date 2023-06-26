from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import (
    TeacherRegisterSerializer,
    StudentRegisterSerializer,
    StudentSerializer,
    UserSerilizer,
    TeacherSerializer,
    GroupSerializer,
)

from rest_framework import status
from .models import Student, Teacher, User, Group
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
        raise AuthenticationFailed("Unaauthenticated")

    user = User.objects.filter(id=payload["id"]).first()
    user_serialzed = UserSerilizer(user)
    print(user_serialzed)

    if user:
        return user
    return False


class StudentRegister(APIView):
    def post(self, request):
        serializer = StudentRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class StudentLoginView(APIView):
    def post(self, request):
        phone_number = request.data["phone_number"]
        password = request.data["password"]
        student = Student.objects.filter(phone_number=phone_number).first()

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

        response.data = {"jwt": token, "role": student.role}

        return response


class StudentRUD(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()

    serializer_class = StudentSerializer
    lookup_field = "pk"

    def delete(self, request, *args, **kwargs):
        user = authenticate(request=request)
        if user:
            print(args)
            print(kwargs)
            print(request)
            if kwargs["pk"] == user.id:
                instance = self.get_object()
                self.perform_destroy(instance)
                return Response({"message": "Object deleted successfully."})
            return Response(
                "you are trying to delete someone's profile",
                status=status.HTTP_403_FORBIDDEN,
            )


class TeacherRegister(APIView):
    def post(self, request):
        serializer = TeacherRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class TeachertLoginView(APIView):
    def post(self, request):
        phone_number = request.data["phone_number"]
        password = request.data["password"]
        teacher = Teacher.objects.filter(phone_number=phone_number).first()

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

        return response


class TeachertRUD(generics.RetrieveUpdateDestroyAPIView):
    queryset = Teacher.objects.all()

    serializer_class = TeacherSerializer
    lookup_field = "pk"

    def delete(self, request, *args, **kwargs):
        user = authenticate(request=request)
        if user:
            if kwargs["pk"] == user.id:
                instance = self.get_object()
                self.perform_destroy(instance)
                return Response({"message": "Object deleted successfully."})
            return Response(
                "you are trying to delete someone's profile",
                status=status.HTTP_403_FORBIDDEN,
            )


class GroupRUD(generics.RetrieveUpdateDestroyAPIView):
    queryset = Group.objects.all()

    serializer_class = GroupSerializer
    lookup_field = "pk"

    def delete(self, request, *args, **kwargs):
        user = authenticate(request=request)
        if user:
            if kwargs["pk"] == user.id:
                instance = self.get_object()
                self.perform_destroy(instance)
                return Response({"message": "Object deleted successfully."})
            return Response(
                "you are trying to delete someone's profile",
                status=status.HTTP_403_FORBIDDEN,
            )


class GroupCL(generics.ListCreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
