"""Загрузка JSON-данных из файла."""

from __future__ import annotations

import json
from pathlib import Path



def load_json_data(file_path: str) -> list[dict] | dict:
    """
    Загружает JSON из указанного файла.

    Args:
        file_path (str): Путь до JSON-файла.

    Returns:
        list[dict] | dict: Содержимое JSON в виде списка словарей или словаря.
    """
    file_data = Path(file_path).read_text(encoding="utf-8")
    return json.loads(file_data)


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Использование: python services/load_json_data.py <file_path>")
    else:
        loaded = load_json_data(sys.argv[1])
        if isinstance(loaded, list):
            print(f"Загружено записей: {len(loaded)}")
        else:
            print(f"Загружен словарь с ключами: {len(loaded.keys())}")
