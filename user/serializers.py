from rest_framework import serializers
from .models import (
    User,
    Group,
    StudentProfile,
    TeacherProfile,
    Attendance,
    Payment,
    WithdrowalBalance,
    Expense,
)


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
    class Meta:
        model = TeacherProfile
        fields = [
            "teleg_account",
        ]


class TeacherRegisterSerializer(serializers.ModelSerializer):
    teacher_profile = TeacherProfileSerializer(required=True)

    class Meta:
        model = User
        fields = ["id", "phone_number", "password", "teacher_profile"]
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
        print(instance.role)
        instance.save()
        print(instance.role)

        return instance


class StudentProfileSerialzer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = [
            "balance",
            "teleg_account",
            "parent_phone",
            "parent_teleg_account",
            "tuition_fee",
        ]


class StudentRegisterSerializer(serializers.ModelSerializer):
    student_profile = StudentProfileSerialzer(required=True)

    class Meta:
        model = User
        fields = ["id", "phone_number", "password", "student_profile"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        student_profile_data = validated_data.pop("student_profile")

        student_profile = StudentProfile.objects.create(
            teleg_account=student_profile_data["teleg_account"],
            parent_phone=student_profile_data["parent_phone"],
            parent_teleg_account=student_profile_data["parent_teleg_account"],
            tuition_fee=student_profile_data["tuition_fee"],
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


class GroupSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Group
        fields = "__all__"


class AttendenceSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Attendance
        fields = "__all__"


class PaymentSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Payment
        fields = "__all__"


class WithdrowalBalanceSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = WithdrowalBalance
        fields = "__all__"


class ExpenseSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Expense
        fields = "__all__"
