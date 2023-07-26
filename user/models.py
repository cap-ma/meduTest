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

    def delete(self, using=None, keep_parents=False):
        # Custom logic before deleting the user
        # For example, you can perform additional actions or checks

        # Delete the user
        super().delete(using=using, keep_parents=keep_parents)


class TeacherProfile(models.Model):
    teleg_account = models.CharField(max_length=50)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.teleg_account)


class Group(models.Model):
    name = models.CharField(max_length=50)
    days = models.CharField(max_length=25)
    date = models.CharField(max_length=15)
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.DO_NOTHING, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class StudentProfile(models.Model):
    class Source(models.TextChoices):
        INSTAGRAM = "INSTAGRAM", "Instagram"
        FACEBOOK = "FACEBOOK", "Facebook"
        TELEGRAM = "TELEGRAM", "Telegram"
        FRIEND = "FRIEND", "Friend"
        LEAFLET = "LEAFLET", "Leaflet"
        OTHER = "OTHER", "Other"

    balance = models.FloatField(default=0)
    teleg_account = models.CharField(max_length=30)
    parent_phone = models.CharField(max_length=13)
    parent_teleg_account = models.CharField(max_length=30)
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.DO_NOTHING, null=True)
    tuition_fee = models.FloatField(default=0)
    source = models.CharField(max_length=10, choices=Source.choices)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    parent_telegram_id = models.CharField(max_length=15, default="")
    verification_for_bot = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)


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
        STUDENT = "STUDENT", "Student"
        TEACHER = "TEACHER", "Teacher"

    role = models.CharField(max_length=50, choices=Role.choices)

    USERNAME_FIELD = "phone_number"
    student_profile = models.OneToOneField(
        StudentProfile, null=True, on_delete=models.SET_NULL
    )
    teacher_profile = models.OneToOneField(
        TeacherProfile, null=True, on_delete=models.SET_NULL
    )

    objects = CustomUserManager()


#


class Attendance(models.Model):
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.DO_NOTHING)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True)
    date = models.DateField()
    student = models.ForeignKey(StudentProfile, on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=25)


class Payment(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.DO_NOTHING)
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.DO_NOTHING)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True)
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
