import re

# -----------------------------
# Валідація client_id
# -----------------------------
# Дозволяємо: букви, цифри, _, -
# Довжина: 3–20 символів
CLIENT_ID_RE = re.compile(r"^[A-Za-z0-9_-]{3,20}$")

def is_valid_client_id(value: str) -> bool:
    return bool(CLIENT_ID_RE.fullmatch(value))


# -----------------------------
# Валідація дати YYYY-MM-DD
# -----------------------------
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

def is_valid_date(value: str) -> bool:
    return bool(DATE_RE.fullmatch(value))


# -----------------------------
# Валідація часу HH:MM:SS
# -----------------------------
TIME_RE = re.compile(r"^[0-2]\d:[0-5]\d:[0-5]\d$")

def is_valid_time(value: str) -> bool:
    return bool(TIME_RE.fullmatch(value))


# -----------------------------
# Валідація суми (дозволяємо 2 знаки після крапки)
# -----------------------------
AMOUNT_RE = re.compile(r"^\d+(\.\d{1,2})?$")

def is_valid_amount(value: str) -> bool:
    return bool(AMOUNT_RE.fullmatch(value))


# -----------------------------
# Валідація кредитного запису (ID операції)
# -----------------------------
CREDIT_ID_RE = re.compile(r"^[A-Z0-9]{5,15}$")

def is_valid_credit_id(value: str) -> bool:
    return bool(CREDIT_ID_RE.fullmatch(value))