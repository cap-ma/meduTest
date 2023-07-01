from rest_framework import serializers
from .models import Student, Teacher, User, Group, StudentProfile, TeacherProfile


class UserSerilizer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {"password": {"write_only": True}}


class TeacherRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ["username", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()

        return instance


class StudentRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ["phone_number", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()

        return instance


class StudentSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Student
        fields = "__all__"
        extra_kwargs = {"password": {"write_only": True}}


class StudentProfileSerialzer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = "__all__"


class TeacherSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Teacher
        fields = "__all__"
        extra_kwargs = {"password": {"write_only": True}}


class TeacherProfileSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = TeacherProfile
        fields = "__all__"


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"
