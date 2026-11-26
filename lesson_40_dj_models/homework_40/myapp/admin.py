from django.contrib import admin
from .models import Category, Transaction, Budget


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "icon", "transaction_count"]
    search_fields = ["name"]

    def transaction_count(self, obj):
        return obj.transactions.count()


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ["date", "user", "category", "amount", "transaction_type"]
    search_fields = ["user__username", "description", "category__name"]
    list_filter = ["transaction_type", "date", "category"]
    date_hierarchy = "date"
    readonly_fields = ["created_at"]


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ["user", "category", "month", "year", "limit", "spent"]
    search_fields = ["user__username", "category__name"]
    list_filter = ["year", "month"]

    def spent(self, obj):
        return f"{obj.get_spent()} ₴"
