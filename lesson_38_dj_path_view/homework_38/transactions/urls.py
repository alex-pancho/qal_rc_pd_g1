from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("transactions/", views.transactions_list, name="transactions_list"),
    path("transactions/<int:transaction_id>/", views.transaction_detail, name="transaction_detail"),
    path("income/", views.income_list, name="income_list"),
    path("expenses/", views.expense_list, name="expense_list"),
    path("budgets/", views.budgets_list, name="budgets_list"),
]
