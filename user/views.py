from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import WithdrowalBalance
from django.shortcuts import get_object_or_404

from .serializers import (
    TeacherRegisterSerializer,
    StudentRegisterSerializer,
    StudentSerializer,
    UserSerilizer,
    TeacherSerializer,
    GroupSerializer,
    StudentProfileSerialzer,
    AttendenceSerializer,
    PaymentSerializer,
    WithdrowalBalanceSerializer,
    ExpenseSerializer,
)

from rest_framework import status
from .models import Student, Teacher, User, Group, StudentProfile, TeacherProfile
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
        return Response(serializer.data)


class StudentRegisterView(APIView):
    def post(self, request):
        user = authenticate(request)

        if user:
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


class StudentProfileRUDView(generics.RetrieveUpdateDestroyAPIView):
    queryset = StudentProfile.objects.all()

    serializer_class = StudentProfileSerialzer
    lookup_field = "pk"

    def retrieve(self, request, *args, **kwargs):
        user = authenticate(request)

        if user:
            if user.role == "TEACHER":
                teacher_id = int(TeacherProfile.objects.get(user__id=user.id).id)
                student_of_teacher = StudentProfile.objects.filter(
                    teacher__id=teacher_id
                ).first()

                if student_of_teacher is not None:
                    instance = self.get_object()

                    serializer = self.get_serializer(instance)
                    return Response(serializer.data)

            else:
                id = StudentProfile.objects.get(user__id=int(user.id))

                if int(id.id) == int(kwargs["pk"]) or ():
                    instance = self.get_object()

                    serializer = self.get_serializer(instance)
                    return Response(serializer.data)

            return Response(
                "You are trying to access someone's profile ",
                status=status.HTTP_403_FORBIDDEN,
            )

    def update(self, request, *args, **kwargs):
        user = authenticate(request)
        if user:
            if user.role == "TAECHER":
                teacher_id = int(TeacherProfile.objects.get(user__id=user.id).id)
                student_of_teacher = StudentProfile.objects.filter(
                    teacher__id=teacher_id
                ).first()

                if student_of_teacher is not None:
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

            else:
                id = StudentProfile.objects.get(user__id=int(user.id))

                if int(id.id) == int(kwargs["pk"]) or ():
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

    def delete(self, request, *args, **kwargs):
        user = authenticate(request=request)
        if user.role == "TEACHER":
            teacher_id = int(TeacherProfile.objects.get(user__id=user.id).id)
            student_of_teacher = StudentProfile.objects.get(teacher__id=teacher_id)
            print(student_of_teacher)
            print(teacher_id, "teacher_iddd")

            if student_of_teacher is not None:
                instance = self.get_object()
                self.perform_destroy(instance)
                return Response({"message": "Object deleted successfully."})
            return Response(
                "you are trying to delete someone's profile",
                status=status.HTTP_403_FORBIDDEN,
            )


class AssignStudentToTeacherView(APIView):
    def put(self, request, id):
        user = authenticate(request)
        if user:
            student_id = int(request.data["student_id"])
            student = StudentProfile.objects.filter(id=student_id).first()
            id = int(user.id)

            teacher_id = TeacherProfile.objects.get(user__id=id)
            teacher_obj = TeacherProfile.objects.filter(id=int(teacher_id)).first()
            student.teacher = teacher_obj
            student.save()
            serialzer_student = StudentProfileSerialzer(student)
            return Response(serialzer_student.data)


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
            return Response(serialzer_student.data)


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

        return Response(serializer.data)


class TeacherRegisterView(APIView):
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


class TeachertRUDView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Teacher.objects.all()

    serializer_class = TeacherSerializer
    lookup_field = "pk"

    def retrieve(self, request, *args, **kwargs):
        user = authenticate(user)
        if user.id == kwargs["ok"]:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)

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

    def update(self, request, *args, **kwargs):
        user = authenticate(request)

        if user.id == kwargs["id"]:
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


class GroupRUDView(APIView):
    def get(self, request, id):
        user = authenticate(request=request)
        if user.role == "Teacher":
            teacher_id = TeacherProfile.objects.get(user__id=int(user.id))
            groups = Group.objects.filter(id=id, teacher__id=teacher_id).first()
            serializer = GroupSerializer(groups)
            return Response(serializer.data)

    def post(self, request):
        user = authenticate(request=request)

        if str(user.role) == "TEACHER":
            name = request.data["name"]

            teacher_id = request.data["teacher"]
            techr_obj = TeacherProfile.objects.filter(id=teacher_id).first()
            groups = Group.objects.create(name=name, teacher=techr_obj)

            serializer = GroupSerializer(groups)
            return Response(serializer.data)


class PaymentView(APIView):
    def post(self, request):
        print(request)
        student = StudentProfile.objects.filter(id=int(request.data["student"])).first()
        student.balance = float(student.balance) + float(request.data["sum"])
        student.save()
        serializer = PaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ExpenseView(APIView):
    def post(self, request):
        serializer = ExpenseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
