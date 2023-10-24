from django.urls import path
from finance.views import TotalPaymentView,ExpenseListView,PaymentListFilterView,IncomeExpenseChartView

urlpatterns=[
    path("total_payment",TotalPaymentView.as_view()),
    path("expenses",ExpenseListView.as_view()),
    path("payments",PaymentListFilterView.as_view()),
    path("income_expense_chart",IncomeExpenseChartView.as_view()),
]