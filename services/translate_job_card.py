"""Перевод значений карточки профессии на русский язык для UI."""

from __future__ import annotations



def translate_job_card(job: dict, description: dict) -> dict:
    """
    Формирует локализованную карточку профессии для отображения в шаблоне.

    Args:
        job (dict): Карточка профессии из `new_jobs.json`.
        description (dict): Словарь переводов из `description.json`.

    Returns:
        dict: Локализованные данные карточки для интерфейса.
    """
    sphere_map = description.get("sphere", {})
    activity_map = description.get("activity", {})
    skills_map = description.get("skills", {})

    level_map = {
        "low": "низкий",
        "medium": "средний",
        "high": "высокий",
    }

    return {
        "id": job.get("id"),
        "title": job.get("title", ""),
        "cluster": job.get("cluster", []),
        "sphere": [sphere_map.get(value, value) for value in job.get("sphere", [])],
        "activity": [
            activity_map.get(value, value) for value in job.get("activity", [])
        ],
        "skills": [skills_map.get(value, value) for value in job.get("skills", [])],
        "why_future": job.get("why_future", ""),
        "tasks": job.get("tasks", []),
        "math_level": level_map.get(job.get("math_level"), job.get("math_level", "")),
        "communication_level": level_map.get(
            job.get("communication_level"),
            job.get("communication_level", ""),
        ),
        "rate": int(job.get("rate", 0)),
    }


if __name__ == "__main__":
    from services.load_json_data import load_json_data

    jobs_data = load_json_data("new_jobs.json")
    desc_data = load_json_data("description.json")
    sample = translate_job_card(jobs_data[0], desc_data)
    print(sample["title"])
