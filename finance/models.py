from django.db import models
from user.models import StudentProfile,TeacherProfile,Group,User


# Create your models here.

class Payment(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.DO_NOTHING)
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.DO_NOTHING)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True)
    sum = models.FloatField()
    comment = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
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

class Expense(models.Model):
    title = models.CharField(max_length=50)
    comment = models.CharField(max_length=100)
    expense_amount = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.DO_NOTHING)
    