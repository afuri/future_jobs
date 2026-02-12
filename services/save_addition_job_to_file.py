"""Сохранение новой профессии в файл пользовательских добавлений."""

from __future__ import annotations

import json
from pathlib import Path


def save_addition_job_to_file(
    file_path: str,
    title: str,
    spheres: list[str],
    skills: list[str],
    why_future: str = "",
    tasks: list[str] | None = None,
) -> dict:
    """
    Добавляет новую профессию в `addition_jobs.json`.

    Args:
        file_path (str): Путь к JSON-файлу с пользовательскими профессиями.
        title (str): Название профессии.
        spheres (list[str]): Список сфер профессии.
        skills (list[str]): Список навыков профессии.
        why_future (str): Пояснение, почему профессия может появиться.
        tasks (list[str] | None): Список задач, которые будет выполнять специалист.

    Returns:
        dict: Сохранённая карточка профессии с присвоенным `id`.
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
    new_job = {
        "id": next_id,
        "title": title,
        "sphere": spheres,
        "skills": skills,
        "why_future": why_future.strip(),
        "tasks": tasks or [],
    }
    existing_data.append(new_job)

    path.write_text(
        json.dumps(existing_data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return new_job


if __name__ == "__main__":
    sample = save_addition_job_to_file(
        "addition_jobs.json",
        "Тестовая профессия",
        ["AI"],
        ["critical_thinking"],
        "Рост спроса на этичные ИИ-решения.",
        ["Оценивать риски", "Консультировать команды"],
    )
    print(sample)
