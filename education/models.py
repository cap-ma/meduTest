from django.db import models

# Create your models here.

from user.models import StudentProfile, TeacherProfile


class TestCategory(models.Model):
    title = models.CharField(max_length=200)
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.SET_NULL, null=True)


class Test(models.Model):
    question = models.CharField(max_length=250)
    a = models.CharField(max_length=200)
    b = models.CharField(max_length=200)
    c = models.CharField(max_length=200)
    d = models.CharField(max_length=200)
    answer = models.CharField(max_length=200)
    level = models.IntegerField()
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.DO_NOTHING)
    category = models.ForeignKey(TestCategory, on_delete=models.SET_NULL, null=True)


class OrderTestInfo(models.Model):
    count = models.IntegerField()
    level = models.IntegerField()
    deadline = models.DateField()
    categories = models.CharField(max_length=300)
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.DO_NOTHING, null=True)


class OrderTestPack(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    order_test_info = models.ForeignKey(OrderTestInfo, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.DO_NOTHING, null=True)


class OrderTestInfoAssignStudent(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    order_test_info = models.ForeignKey(OrderTestInfo, on_delete=models.CASCADE)
    submitted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.SET_NULL, null=True)


class OrderTestPackResultsOfStudent(models.Model):
    result = models.CharField(max_length=200)
    student = models.ForeignKey(
        OrderTestInfoAssignStudent, on_delete=models.SET_NULL, null=True
    )
    is_correct = models.BooleanField(null=True)
    order_test_info = models.ForeignKey(
        OrderTestInfo, on_delete=models.CASCADE, null=True
    )
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.DO_NOTHING)
