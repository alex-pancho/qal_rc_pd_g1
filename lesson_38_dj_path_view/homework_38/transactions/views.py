from django.shortcuts import render
from django.http import HttpResponse

# Тимчасові дані
TRANSACTIONS = [
    {"id": 1, "amount": 30000, "type": "income", "category": "Salary", "date": "2024-01-15", "description": "Зарплата за січень"},
    {"id": 2, "amount": 5000, "type": "expense", "category": "Food", "date": "2024-01-16", "description": "Продукти"},
    {"id": 3, "amount": 3000, "type": "expense", "category": "Transport", "date": "2024-01-17", "description": "Бензин"},
    {"id": 4, "amount": 15000, "type": "income", "category": "Freelance", "date": "2024-01-18", "description": "Проєкт для клієнта"},
]

BUDGETS = [
    {"category": "Food", "monthly_limit": 10000},
    {"category": "Transport", "monthly_limit": 5000},
    {"category": "Entertainment", "monthly_limit": 3000},
]


def home(request):
    """Головна"""
    total_income = sum(t["amount"] for t in TRANSACTIONS if t["type"] == "income")
    total_expense = sum(t["amount"] for t in TRANSACTIONS if t["type"] == "expense")
    balance = total_income - total_expense
    context = {
        "title": "Expense Tracker",
        "total_income": total_income,
        "total_expense": total_expense,
        "balance": balance,
    }
    return render(request, "transactions/home.html", context)


def transactions_list(request):
    """Список всіх транзакцій"""
    context = {
        "title": "Мої транзакції",
        "transactions": TRANSACTIONS,
    }
    return render(request, "transactions/transactions_list.html", context)


def transaction_detail(request, transaction_id):
    """Деталі транзакції"""
    transaction = next((t for t in TRANSACTIONS if t["id"] == transaction_id), None)
    if transaction is None:
        return HttpResponse("Транзакція не знайдена", status=404)
    context = {"transaction": transaction}
    return render(request, "transactions/transaction_detail.html", context)


def budgets_list(request):
    """Список бюджетів"""
    context = {
        "title": "Бюджети",
        "budgets": BUDGETS,
    }
    return render(request, "transactions/budgets_list.html", context)


def income_list(request):
    """Тільки доходи"""
    income_transactions = [t for t in TRANSACTIONS if t["type"] == "income"]
    total = sum(t["amount"] for t in income_transactions)
    context = {
        "title": "Доходи",
        "transactions": income_transactions,
        "total": total,
    }
    return render(request, "transactions/transactions_list.html", context)


def expense_list(request):
    """Тільки витрати"""
    expense_transactions = [t for t in TRANSACTIONS if t["type"] == "expense"]
    total = sum(t["amount"] for t in expense_transactions)
    context = {
        "title": "Витрати",
        "transactions": expense_transactions,
        "total": total,
    }
    return render(request, "transactions/transactions_list.html", context)

