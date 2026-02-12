"""Получение значений для фильтров интерфейса."""

from __future__ import annotations



def get_filter_options(jobs: list[dict]) -> dict[str, list[str]]:
    """
    Возвращает уникальные сферы и навыки из списка профессий.

    Args:
        jobs (list[dict]): Список карточек профессий.

    Returns:
        dict[str, list[str]]: Словарь с ключами `sphere` и `skills`.
    """
    spheres = sorted({sphere for job in jobs for sphere in job.get("sphere", [])})
    skills = sorted({skill for job in jobs for skill in job.get("skills", [])})
    return {"sphere": spheres, "skills": skills}


if __name__ == "__main__":
    from services.load_json_data import load_json_data

    jobs_data = load_json_data("new_jobs.json")
    options = get_filter_options(jobs_data)
    print(f"Сфер: {len(options['sphere'])}")
    print(f"Навыков: {len(options['skills'])}")
