import pytest

# --- Частина 1. Базові запити (Завдання 1-3) ---


def test_task_1_get_all_posts(api_client):
    """Завдання 1: Отримати всі posts (перевірка 200 та кількості 100)."""
    response = api_client.make_request("GET", "/posts")

    assert response.status_code == 200
    posts = response.json()
    assert len(posts) == 100, f"Очікували 100 записів, отримали {len(posts)}"


def test_task_2_get_post_by_id_10(api_client):
    """Завдання 2: Отримати post з id=10 та перевірити наявність необхідних полів."""
    response = api_client.make_request("GET", "/posts/10")

    assert response.status_code == 200
    data = response.json()

    assert data["id"] == 10
    required_fields = ["userId", "id", "title", "body"]
    for field in required_fields:
        assert field in data, f"Поле {field} відсутнє у відповіді"


def test_task_3_get_todos_by_user_id_2(api_client):
    """Завдання 3: Отримати всі todos користувача userId=2."""
    response = api_client.make_request("GET", "/todos", params={"userId": 2})

    assert response.status_code == 200
    todos = response.json()

    assert len(todos) > 0, "Список todos порожній"
    for todo in todos:
        assert todo["userId"] == 2, f"Очікували userId=2, але є {todo['userId']}"


# --- Частина 2. CRUD (Завдання 4-7) ---


def test_task_4_create_post(api_client):
    """Завдання 4: Створити новий post (POST)."""
    payload = {
        "title": "New Auto Test Post",
        "body": "Content for testing API",
        "userId": 1,
    }

    response = api_client.make_request("POST", "/posts", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == payload["title"]
    assert data["body"] == payload["body"]


def test_task_5_update_post_put(api_client):
    """Завдання 5: Оновити post id=5 (PUT)."""
    payload = {
        "id": 5,
        "title": "Updated Title",
        "body": "Updated Body",
        "userId": 1,
    }

    response = api_client.make_request("PUT", "/posts/5", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == payload["title"]
    assert data["body"] == payload["body"]


def test_task_6_partial_update_patch(api_client):
    """Завдання 6: Частково оновити title у post id=5 (PATCH)."""
    payload = {"title": "Patched Title Only"}

    response = api_client.make_request("PATCH", "/posts/5", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == payload["title"]


def test_task_7_delete_post(api_client):
    """Завдання 7: Видалити post id=5 (DELETE)."""
    response = api_client.make_request("DELETE", "/posts/5")

    assert response.status_code in [200, 204]


# --- Частина 3. Негативні сценарії (Завдання 8-9) ---


def test_task_8_get_non_existing_post(api_client):
    """Завдання 8: Отримати неіснуючий post id=999999."""
    response = api_client.make_request("GET", "/posts/999999")

    assert response.status_code == 404 or response.json() == {}


def test_task_9_post_empty_body(api_client):
    """Завдання 9: Відправити порожнє тіло запиту (POST {})."""
    response = api_client.make_request("POST", "/posts", json={})

    # JSONPlaceholder приймає порожні об'єкти та повертає 201 зі згенерованим ID
    assert response.status_code in [201, 400]
    data = response.json()
    assert "id" in data


# --- Частина 4. Робота з headers (Завдання 10) ---


def test_task_10_custom_headers(api_client):
    """Завдання 10: Відправити GET з custom headers."""
    custom_headers = {"User-Agent": "QA Student"}

    response = api_client.make_request(
        "GET", "/posts", headers=custom_headers
    )

    assert response.status_code == 200


# --- Bonus ⭐ та Assertions (Завдання 11-12) ---


def test_task_11_12_make_request_with_assertions(api_client):
    """Завдання 11 та 12: Перевірка універсальної функції з pytest assertions."""
    # Перевірка GET
    get_res = api_client.make_request("GET", "/posts")
    assert get_res.status_code == 200
    assert len(get_res.json()) == 100

    # Перевірка POST
    post_data = {"title": "Bonus Test", "body": "Bonus Body", "userId": 1}
    post_res = api_client.make_request("POST", "/posts", json=post_data)
    assert post_res.status_code == 201
    assert post_res.json()["title"] == "Bonus Test"