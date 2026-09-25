import requests


class APIClient:

    def __init__(self, base_url: str):
        self.base_url = base_url

    def make_request(self, method: str, endpoint: str, **kwargs):
        """Універсальний метод для виконання HTTP-запитів (Завдання 11)."""
        url = f"{self.base_url}{endpoint}"
        return requests.request(method=method, url=url, **kwargs)