from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    """Категорії видатків: їжа, транспорт, розваги тощо"""
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=20, blank=True)  # emoji або іконка
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Transaction(models.Model):
    TYPE_CHOICES = [
        ("income", "Дохід"),
        ("expense", "Видаток"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="transactions"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name="transactions"
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Сума в гривнях"
    )
    transaction_type = models.CharField(
        max_length=10,
        choices=TYPE_CHOICES
    )
    date = models.DateField()
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Транзакція"
        verbose_name_plural = "Транзакції"
        ordering = ["-date"]
        indexes = [
            models.Index(fields=["user", "-date"]),
            models.Index(fields=["transaction_type"]),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.amount} ₴ ({self.get_transaction_type_display()})"


class Budget(models.Model):
    """Бюджет: ліміт видатків на місяць за категорією"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="budgets"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE
    )
    month = models.IntegerField()  # 1-12
    year = models.IntegerField()
    limit = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Максимальна сума видатків на місяць"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Бюджет"
        verbose_name_plural = "Бюджети"
        unique_together = ["user", "category", "month", "year"]
        ordering = ["-year", "-month"]

    def __str__(self):
        return f"{self.user.username} - {self.category} ({self.month}/{self.year}): {self.limit} ₴"

    def get_spent(self):
        """Скільки вже витрачено цього місяця за цією категорією"""
        spent = Transaction.objects.filter(
            user=self.user,
            category=self.category,
            transaction_type="expense",
            date__month=self.month,
            date__year=self.year
        ).aggregate(total=models.Sum("amount"))["total"] or 0
        return spent

    def get_remaining(self):
        """Скільки ще можна витратити"""
        return self.limit - self.get_spent()

    def is_exceeded(self):
        """Чи перевищено ліміт"""
        return self.get_spent() > self.limit
