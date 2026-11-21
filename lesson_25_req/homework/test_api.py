import requests

BASE_URL = "https://jsonplaceholder.typicode.com"


# Bonus: Завдання 11 — Універсальна функція для запитів
def make_request(method, endpoint, **kwargs):
    url = f"{BASE_URL}{endpoint}"
    return requests.request(method, url, **kwargs)


# --- Частина 1. Базові запити (GET) ---

# Завдання 1
def test_get_all_posts():
    response = make_request("GET", "/posts")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 100


# Завдання 2
def test_get_post_by_id():
    response = make_request("GET", "/posts/10")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 10
    expected_keys = {"userId", "id", "title", "body"}
    assert expected_keys.issubset(data.keys())


# Завдання 3
def test_get_todos_by_user_id():
    response = make_request("GET", "/todos", params={"userId": 2})
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert all(todo["userId"] == 2 for todo in data)


# --- Частина 2. CRUD ---

# Завдання 4 — Create
def test_create_post():
    payload = {
        "title": "QA Automation Post",
        "body": "Testing POST request with pytest",
        "userId": 1,
    }
    response = make_request("POST", "/posts", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == payload["title"]
    assert data["body"] == payload["body"]
    assert "id" in data


# Завдання 5 — Update через PUT
def test_update_post_put():
    payload = {
        "id": 5,
        "title": "Updated Title via PUT",
        "body": "Completely updated body",
        "userId": 1,
    }
    response = make_request("PUT", "/posts/5", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == payload["title"]
    assert data["body"] == payload["body"]
    assert data["userId"] == payload["userId"]


# Завдання 6 — Partial Update через PATCH
def test_partial_update_post_patch():
    payload = {"title": "Patched Title Only"}
    response = make_request("PATCH", "/posts/5", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == payload["title"]
    assert "body" in data  # Переконуємося, що інші поля залишилися на місці


# Завдання 7 — Delete
def test_delete_post():
    response = make_request("DELETE", "/posts/5")
    assert response.status_code in (200, 204)


# --- Частина 3. Негативні сценарії ---

# Завдання 8
def test_get_nonexistent_post():
    response = make_request("GET", "/posts/999999")
    assert response.status_code == 404 or response.json() == {}


# Завдання 9
def test_create_post_empty_body():
    # JSONPlaceholder є mock-API, тому він приймає порожній об'єкт і повертає 201 + лише згенерований id
    response = make_request("POST", "/posts", json={})
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert "title" not in data


# --- Частина 4. Робота з headers ---

# Завдання 10
def test_get_with_custom_headers():
    custom_headers = {"User-Agent": "QA Student"}
    response = make_request("GET", "/posts/1", headers=custom_headers)
    assert response.status_code == 200
    assert response.request.headers["User-Agent"] == "QA Student"
