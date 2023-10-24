from rest_framework import serializers
from .models import (
    User,
    Group,
    StudentProfile,
    TeacherProfile,
    Attendance,
   
    WithdrowalBalance,
    
    UserTraffic,
    Sms,
)

from finance.models import Payment,Expense

class UserSerilizer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        instance = self.Meta.model(**validated_data)

        if password is not None:
            instance.set_password(password)
        instance.save()

        return instance



class TeacherProfileSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = TeacherProfile
        fields = [
            "id",
            "teleg_account",
        ]


class TeacherGetMeSerailizer(serializers.ModelSerializer):
    teacher_profile = TeacherProfileSerializer(required=True)

    class Meta:
        model = User
        fields = [
            "id",
            "phone_number",
            "first_name",
            "last_name",
            "role",
            "teacher_profile",
        ]


class TeacherRegisterSerializer(serializers.ModelSerializer):
    teacher_profile = TeacherProfileSerializer(required=True)

    class Meta:
        model = User
        fields = [
            "id",
            "phone_number",
            "password",
            "first_name",
            "last_name",
            "teacher_profile",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        password = validated_data.pop("password", None)

        teacher_profile_data = validated_data.pop("teacher_profile")

        teacher_profile = TeacherProfile.objects.create(
            teleg_account=teacher_profile_data["teleg_account"]
        )
        instance = self.Meta.model(**validated_data)

        if password is not None:
            instance.set_password(password)
        instance.teacher_profile = teacher_profile
        instance.role = "TEACHER"

        instance.save()

        UserTraffic.objects.create(teacher=teacher_profile)

        return instance


class StudentProfileSerialzer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = [
            "id",
            "balance",
            "teleg_account",
            "parent_phone",
            "parent_teleg_account",
            "tuition_fee",
            "teacher",
            "source",
        ]


class StudentGetMeSerializer(serializers.ModelSerializer):
    student_profile = StudentProfileSerialzer(required=True)

    class Meta:
        model = User
        fields = [
            "phone_number",
            "first_name",
            "last_name",
            "role",
            "student_profile",
        ]


class StudentFilterListViewSerializer(serializers.ModelSerializer):
    student_profile = StudentProfileSerialzer(required=True)

    class Meta:
        model = User
        fields = [
            "phone_number",
            "first_name",
            "last_name",
            "student_profile",
        ]


class StudentRegisterSerializer(serializers.ModelSerializer):
    student_profile = StudentProfileSerialzer(required=True)

    class Meta:
        model = User
        fields = [
            "id",
            "phone_number",
            "password",
            "first_name",
            "last_name",
            "student_profile",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        student_profile_data = validated_data.pop("student_profile")
        
        student_profile = StudentProfile.objects.create(
            teleg_account=student_profile_data["teleg_account"],
            parent_phone=student_profile_data["parent_phone"],
            parent_teleg_account=student_profile_data["parent_teleg_account"],
            tuition_fee=student_profile_data["tuition_fee"],
            source=student_profile_data["source"],
        )

        password = validated_data.pop("password", None)

        instance = self.Meta.model(**validated_data)
        instance.role = "STUDENT"

        if password is not None:
            instance.set_password(password)
        instance.student_profile = student_profile
        instance.save()

        return instance


class StudentProfileSerialzer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = StudentProfile
        fields = "__all__"


class StudentUpdateSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField()
    last_name = serializers.CharField()
    first_name = serializers.CharField()

    class Meta:
        model = StudentProfile
        fields = ["phone_number", "last_name", "first_name"]


class GroupSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Group
        fields = "__all__"


class AttendenceSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Attendance
        fields = "__all__"


class WithdrowalBalanceSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = WithdrowalBalance
        fields = "__all__"




class StudentIncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTraffic
        fields = "__all__"
class SmsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Sms
        fields="__all__"
