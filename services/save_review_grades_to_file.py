"""Сохранение оценок отзыва о стажировке в JSON-файл."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path


def save_review_grades_to_file(
    file_path: str,
    grades: dict[str, int],
) -> dict:
    """
    Сохраняет новый отзыв с оценками в файл `grades.json`.

    Args:
        file_path (str): Путь до JSON-файла с отзывами.
        grades (dict[str, int]): Оценки пользователя по вопросам в формате `{"q1": 5, ...}`.

    Returns:
        dict: Сохранённая запись отзыва с `id`, временем отправки и оценками.
    """
    path = Path(file_path)

    existing_data: list[dict] = []
    if path.exists():
        try:
            parsed = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(parsed, list):
                existing_data = parsed
        except json.JSONDecodeError:
            existing_data = []

    next_id = max((int(item.get("id", 0)) for item in existing_data), default=0) + 1
    review_entry = {
        "id": next_id,
        "submitted_at": datetime.now(timezone.utc).isoformat(),
        "grades": grades,
    }
    existing_data.append(review_entry)

    path.write_text(
        json.dumps(existing_data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return review_entry


if __name__ == "__main__":
    sample_entry = save_review_grades_to_file(
        "grades.json",
        {"q1": 5, "q2": 4, "q3": 5},
    )
    print(sample_entry["id"])
