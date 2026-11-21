import csv
import json
from datetime import datetime
from pathlib import Path
from models import Transaction, TransactionNotFoundError


class Budget:
    def __init__(self, data_file: str):
        self.data_path = Path(data_file)
        self.data_path.parent.mkdir(parents=True, exist_ok=True)
        self.transactions: list[Transaction] = self._load()

    def _load(self) -> list[Transaction]:
        if not self.data_path.exists():
            return []
        with open(self.data_path, encoding="utf-8") as f:
            raw_data = json.load(f)
            return [Transaction.from_dict(item) for item in raw_data]

    def _save(self) -> None:
        with open(self.data_path, "w", encoding="utf-8") as f:
            json.dump([t.to_dict() for t in self.transactions], f, ensure_ascii=False, indent=2)

    def _next_id(self) -> int:
        if not self.transactions:
            return 1
        return max(t.id for t in self.transactions if t.id is not None) + 1

    def add_transaction(self, transaction: Transaction) -> Transaction:
        transaction.id = self._next_id()
        self.transactions.append(transaction)
        self._save()
        return transaction

    def delete_transaction(self, t_id: int) -> Transaction:
        for i, t in enumerate(self.transactions):
            if t.id == t_id:
                removed = self.transactions.pop(i)
                self._save()
                return removed
        raise TransactionNotFoundError(f"Транзакцію з ID {t_id} не знайдено.")

    def list_transactions(self, t_type: str | None = None, category: str | None = None) -> list[Transaction]:
        result = self.transactions
        if t_type:
            result = [t for t in result if t.transaction_type == t_type]
        if category:
            result = [t for t in result if t.category.lower() == category.lower()]
        return result

    def calculate_balance(self) -> float:
        balance = 0.0
        for t in self.transactions:
            if t.transaction_type == "income":
                balance += t.amount
            elif t.transaction_type == "expense":
                balance -= t.amount
        return balance

    def monthly_report(self) -> tuple[float, float]:
        current_month = datetime.now().strftime("%Y-%m")
        income_total = 0.0
        expense_total = 0.0

        for t in self.transactions:
            if t.date.startswith(current_month):
                if t.transaction_type == "income":
                    income_total += t.amount
                elif t.transaction_type == "expense":
                    expense_total += t.amount
        return income_total, expense_total

    def export_data(self, fmt: str, export_dir: str) -> Path:
        out_dir = Path(export_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = out_dir / f"transactions_{timestamp}.{fmt}"

        if fmt == "json":
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump([t.to_dict() for t in self.transactions], f, ensure_ascii=False, indent=2)
        elif fmt == "csv":
            fieldnames = ["id", "date", "transaction_type", "category", "amount", "description"]
            with open(file_path, "w", newline="", encoding="utf-8-sig") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                for t in self.transactions:
                    writer.writerow(t.to_dict())

        return file_path
