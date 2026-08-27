from abc import ABC, abstractmethod


class Report(ABC):
    """Абстрактний базовий клас для всіх звітів"""

    def __init__(self, title: str):
        self.title = title

    @abstractmethod
    def generate(self) -> str:
        """Кожен підклас зобов'язаний реалізувати цей метод"""
        pass

    @abstractmethod
    def save(self, filepath: str) -> None:
        """Зберегти звіт у файл"""
        pass

    def preview(self) -> str:
        """Конкретний метод — спільний для всіх підкласів"""
        return f"[Попередній перегляд: {self.title}]"

class PDFReport(Report):
    def __init__(self, title):
        super().__init__(title)

    def generate(self) -> str:
        return f"PDF звіт: {self.title}"

    def save(self, filepath: str = "") -> None:
        print(f"Збереження PDF у {filepath}")


report = PDFReport("Квартальний звіт")
print(report.generate())
print(report.preview())