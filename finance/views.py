from django.shortcuts import render
from django.db.models import Sum

from rest_framework import  generics
from rest_framework.views import APIView
from rest_framework.response import Response

from finance.models import Payment,Expense
from user.views import authenticate
from .serializers import ExpenseSerializer,PaymentSerializerForFinance,PaymentSerializer

import datetime
from datetime import datetime , timedelta,date

def get_first_date_of_current_month(year, month):
    """Return the first date of the month.

    Args:
        year (int): Year
        month (int): Month

    Returns:
        date (datetime): First date of the current month
    """

    first_date = datetime(year, month, 1)
    return first_date


def get_last_date_of_month(year, month):
    """Return the last date of the month.
    
    Args:
        year (int): Year, i.e. 2022
        month (int): Month, i.e. 1 for January

    Returns:
        date (datetime): Last date of the current month
    """
    
    if month == 12:
        last_date = datetime(year, month, 31)
    else:
        last_date = datetime(year, month + 1, 1) + timedelta(days=-1)
    return last_date

class TotalPaymentView(APIView):
    def get(self,request):
        user=authenticate(request)
        if user.role=="TEACHER":
            payments=Payment.objects.filter(teacher=user.teacher_profile)
            total_payment=payments.aggregate(Sum("sum"))
            print(total_payment)
            return Response(total_payment,200)
        return Response({"error":"Forbidden"},404)
    
class PaymentListFilterView(APIView):
    def get(self,request):
        user=authenticate(request)
        if user.role=="TEACHER":
            phone_number=request.query_params.get("phone")
            full_name=request.query_params.get("full_name")
            from_date_timestamp=request.query_params.get("from")
           
            to_date_timestamp=request.query_params.get("to")
            if from_date_timestamp:
                from_date=date.fromtimestamp(float(from_date_timestamp))
            if to_date_timestamp:
                to_date=date.fromtimestamp(float(to_date_timestamp))



            qs=Payment.objects.filter(teacher=user.teacher_profile)
           
            if phone_number is not None and phone_number!="":
                qs=qs.filter(student__user__phone_number__contains=phone_number)
             
            if (full_name is not None and full_name!=""):
                qs=qs.filter(student__user__first_name__contains=full_name)
            if (full_name is not None and full_name !=""):
                qs=qs.filter(student__user__last_name__contains=full_name)
            if from_date_timestamp is not None and from_date_timestamp!="":
                qs=qs.filter(created_at__gt=from_date)
            if to_date_timestamp is not None and to_date_timestamp!="":
                qs=qs.filter(created_at__lt=to_date)

            serializer=PaymentSerializerForFinance(qs,many=True)
            return Response(serializer.data,200)
            
class ExpenseListView(APIView):
    def get(self,request):
        user=authenticate(request)
        if user.role=="TEACHER":
            expenses=Expense.objects.filter(teacher=user.teacher_profile) 
            serializer=ExpenseSerializer(expenses,many=True)
            return Response(serializer.data,200)
        return Response({"message":"Forbidden"},404)
    

class IncomeExpenseChartView(APIView):
    def get(self,request):
        user=authenticate(request)
        if user.role=="TEACHER":
            try:
                type_of_time=request.query_params.get("type")
            except Exception:
                return Response({"message":"No type data provided"},404)
            try:

                time=request.query_params.get("time")
            except Exception:
                return Response({"message":"No time data provided"},404)
            
            print(type_of_time)        
            # time_list=time.split("-")
            time_converted=date.fromtimestamp(float(time)) 
            """(year=int(time_list[0]),month=int(time_list[1]),day=int(time_list[2]))"""
            year=time_converted.year

            if type_of_time=="monthly":
                payment_expense_dict={}
                if time:
                    expenses=Expense.objects.filter(teacher=user.teacher_profile,created_at__gt=time_converted)
                    payments=Payment.objects.filter(teacher=user.teacher_profile,created_at__gt=time_converted)
                    print(payments)
                    payment_serializer=PaymentSerializer(payments,many=True)
                    expense_serializer=ExpenseSerializer(expenses,many=True)
                    payment_expense_dict["payment"]=payment_serializer.data
                    payment_expense_dict["expense"]=expense_serializer.data

                    return Response(payment_expense_dict)

            elif(type_of_time=="yearly"):
            
                payments=Payment.objects.filter(teacher=user.teacher_profile)
                expenses=Expense.objects.filter(teacher=user.teacher_profile)

                my_dict_payment={}
                my_dict_expense={}
                my_list=[]
                payment_expense_dict={}
                print(time_converted.month,"month")
                for x in range(int(time_converted.month)):    
                           
                    month=x+1

                    print(month,"heeereee")
                    first_date=get_first_date_of_current_month(year,month)
                    last_date=get_last_date_of_month(year,month)
                    monthly_payments=payments.filter(created_at__gte=first_date,created_at__lte=last_date)
                    expense_payments=expenses.filter(created_at__gte=first_date,created_at__lte=last_date)
                    summation_monthly_payment=monthly_payments.aggregate(Sum("sum"))
                    summation_monthly_expense=expense_payments.aggregate(Sum("expense_amount"))

                    my_dict_payment[f"{year}-{month}"]=summation_monthly_payment
                    my_dict_expense[f"{year}-{month}"]=summation_monthly_expense
                    payment_expense_dict["payment"]=my_dict_payment
                    payment_expense_dict["expense"]=my_dict_expense

                my_list.append(payment_expense_dict)
                   
               
                print(my_list,"`````````````````")

                return Response(my_list)


    









            
            




