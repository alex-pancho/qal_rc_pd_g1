import os
import configparser
from pathlib import Path


def load_env(env_path: str = ".env") -> None:
    path = Path(env_path)
    if not path.exists():
        return
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, _, value = line.partition("=")
                os.environ.setdefault(key.strip(), value.strip())


def load_config(config_path: str = "config.ini") -> configparser.ConfigParser:
    config = configparser.ConfigParser()
    config.read(config_path, encoding="utf-8")
    return config


def get_settings() -> dict:
    load_env()
    config = load_config()

    return {
        "debug": os.getenv("DEBUG", "false").lower() == "true",
        "log_level": os.getenv("LOG_LEVEL", "INFO"),
        "user_name": os.getenv("USER_NAME", "User"),
        "app_name": config.get("app", "name", fallback="Expense Tracker"),
        "app_version": config.get("app", "version", fallback="0.3.0"),
        "currency": config.get("app", "currency", fallback="грн"),
        "data_file": config.get("storage", "data_file", fallback="data/transactions.json"),
        "export_dir": config.get("storage", "export_dir", fallback="exports/"),
    }
