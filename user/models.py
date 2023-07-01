from django.db import models
from django.contrib.auth.models import BaseUserManager

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db.models.query import QuerySet
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import RegexValidator


class User(AbstractUser):
    username = None
    email = models.EmailField(blank=True, null=True)
    phone_regex = RegexValidator(
        regex=r"^\+?1?\d{9,13}$", message="must be in this format: +998999999999 "
    )
    phone_number = models.CharField(
        max_length=13, validators=[phone_regex], unique=True
    )

    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        STUDENT = "STUDENT", "Student"
        TEACHER = "TEACHER", "Teacher"

    base_role = Role.ADMIN

    role = models.CharField(max_length=50, choices=Role.choices)

    USERNAME_FIELD = "phone_number"

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.base_role

            return super().save(*args, **kwargs)


class TeacherManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.TEACHER)


class Teacher(User):
    base_role = User.Role.TEACHER

    class Meta:
        proxy = True

    def welcome(self):
        return "teacher"

    student = TeacherManager()


@receiver(post_save, sender=Teacher)
def create_teacher_profile(sender, instance, created, **kwargs):
    if created and instance.role == "TEACHER":
        TeacherProfile.objects.create(user=instance)


class TeacherProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    telegAccount = models.CharField(max_length=50)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


class Group(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.DO_NOTHING)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


class StudentManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.STUDENT)


class Student(User):
    base_role = User.Role.STUDENT

    class Meta:
        proxy = True

    def welcome(self):
        return "students"

    student = StudentManager()


@receiver(post_save, sender=Student)
def create_student_profile(sender, instance, created, **kwargs):
    if created and instance.role == "STUDENT":
        StudentProfile.objects.create(user=instance)


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    balance = models.FloatField()
    telegAccount = models.CharField(max_length=30)
    parentPhone = models.CharField(max_length=13)
    parentTelegAccount = models.CharField(max_length=30)
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.DO_NOTHING, null=True)
    tuitionFee = models.FloatField()
    group = models.ForeignKey(Group, on_delete=models.DO_NOTHING, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
