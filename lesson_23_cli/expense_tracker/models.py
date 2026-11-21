from datetime import datetime
from enum import Enum


class InvalidAmountError(Exception):
    pass


class TransactionNotFoundError(Exception):
    pass


class TransactionType(Enum):
    INCOME = "income"
    EXPENSE = "expense"


class User:
    def __init__(self, username: str):
        self.username = username


class Transaction:
    def __init__(
        self,
        amount: float,
        transaction_type: str,
        category: str,
        description: str = "",
        t_id: int | None = None,
        date: str | None = None,
    ):
        if amount <= 0:
            raise InvalidAmountError("Сума повинна бути більшою за 0!")

        self.id = t_id
        self.amount = float(amount)
        self.transaction_type = transaction_type
        self.category = category
        self.description = description
        self.date = date or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "amount": self.amount,
            "transaction_type": self.transaction_type,
            "category": self.category,
            "description": self.description,
            "date": self.date,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Transaction":
        return cls(
            t_id=data["id"],
            amount=data["amount"],
            transaction_type=data["transaction_type"],
            category=data["category"],
            description=data.get("description", ""),
            date=data.get("date"),
        )
