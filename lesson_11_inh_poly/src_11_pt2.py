from datetime import datetime


class Task:
    """Базовий клас завдання"""

    task_count = 0  # атрибут класу

    def __init__(self, title: str, description: str = ""):
        Task.task_count += 1
        self.id = Task.task_count
        self.title = title
        self.description = description
        self.created_at = datetime.now()
        self.is_done = False

    def complete(self) -> None:
        self.is_done = True

    def status(self) -> str:
        return "✅" if self.is_done else "⏳"

    def __repr__(self) -> str:
        return f"[{self.status()}] #{self.id} {self.title}"

    @classmethod
    def get_count(cls) -> int:
        return cls.task_count

    @staticmethod
    def validate_title(title: str) -> bool:
        return bool(title) and len(title) <= 100


class UrgentTask(Task):
    """Термінове завдання з дедлайном"""

    def __init__(self, title: str, deadline: datetime, description: str = ""):
        super().__init__(title, description)
        self.deadline = deadline

    def is_overdue(self) -> bool:
        return datetime.now() > self.deadline and not self.is_done

    def status(self) -> str:  # поліморфізм
        if self.is_overdue():
            return "🔥"
        return super().status()


class RecurringTask(Task):
    """Завдання, що повторюється"""

    def __init__(self, title: str, interval_days: int, description: str = ""):
        super().__init__(title, description)
        self.interval_days = interval_days

    def status(self) -> str:  # поліморфізм
        return f"🔄({self.interval_days}д)"


# --- Використання ---
tasks: list[Task] = [
    Task("Прочитати документацію"),
    UrgentTask("Здати звіт", datetime(2026, 8, 8)),  # минулий дедлайн
    RecurringTask("Щоденний стендап", 1),
]

for task in tasks:
    print(task)  # поліморфний виклик __repr__ і status()

print(f"\nВсього завдань створено: {task.get_count()}")
print(f"Валідна назва 'Test': {Task.validate_title('Test')}")
print(f"Валідна назва '': {Task.validate_title('')}")