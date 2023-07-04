from django.db import models
from django.contrib.auth.models import BaseUserManager

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db.models.query import QuerySet
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import RegexValidator


from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, phone_number, password, **extra_fields):
        """
        Create and save a user with the given phone_number and password.
        """
        if not phone_number:
            raise ValueError(_("The phone_number must be set"))

        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, phone_number, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(
            email, phone_number=phone_number, password=password, **extra_fields
        )


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

    objects = CustomUserManager()


class TeacherManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.TEACHER)


#


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

    def __str__(self):
        return str(self.user)


class Group(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.DO_NOTHING, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class StudentManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        print(results, "resultssssss")
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
        print(instance, "it is instanceeee")
        print(kwargs)
        print(created, "sender")
        StudentProfile.objects.create(user=instance)


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    balance = models.FloatField(null=True)
    telegAccount = models.CharField(max_length=30)
    parentPhone = models.CharField(max_length=13)
    parentTelegAccount = models.CharField(max_length=30)
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.DO_NOTHING, null=True)
    tuitionFee = models.FloatField(null=True)
    group = models.ForeignKey(Group, on_delete=models.DO_NOTHING, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user)


class Attendance(models.Model):
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.DO_NOTHING)
    group = models.ForeignKey(Group, on_delete=models.DO_NOTHING)
    date = models.DateField()
    student = models.ForeignKey(StudentProfile, on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=25)


class Payment(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.DO_NOTHING)
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.DO_NOTHING)
    group = models.ForeignKey(Group, on_delete=models.DO_NOTHING)
    sum = models.FloatField()
    comment = models.CharField(max_length=50, null=True, blank=True)

    NAQT = "NAQT"
    PLASTIK = "PLASTIK"
    BOSHQA = "BOSHQA"

    PAYMENT_TYPE = [
        (NAQT, "naqt"),
        (PLASTIK, "plastik"),
        (BOSHQA, "boshqa"),
    ]
    payment_type = models.CharField(
        max_length=7,
        choices=PAYMENT_TYPE,
        default=NAQT,
    )


class WithdrowalBalance(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.DO_NOTHING)
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.DO_NOTHING)
    balance = models.FloatField()
    created_at = models.DateTimeField(auto_now=True)


class Expense(models.Model):
    title = models.CharField(max_length=50)
    comment = models.CharField(max_length=100)
    expense_amount = models.FloatField()
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.DO_NOTHING)
