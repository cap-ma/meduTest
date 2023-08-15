from rest_framework import serializers
from .models import Payment,Expense
from user.models import User,StudentProfile


class UserForPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=["phone_number","first_name","last_name"]

class StudentProfileSerializerForFinance(serializers.ModelSerializer):
    phone_number=serializers.CharField(source="user.phone_number")
    first_name=serializers.CharField(source="user.first_name")
    last_name=serializers.CharField(source="user.last_name")



    class Meta:
        model=StudentProfile
        fields=["id","phone_number","first_name","last_name","parent_phone"]

class PaymentSerializerForFinance(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    student=StudentProfileSerializerForFinance()
    
    class Meta:
        model = Payment
        fields = ["id", "student", "teacher", "sum", "comment", "payment_type"]

class PaymentSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
  
    
    class Meta:
        model = Payment
        fields = ["id", "student", "teacher", "sum", "comment", "payment_type"]

class ExpenseSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Expense
        fields = "__all__"
