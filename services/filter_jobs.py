"""Фильтрация списка профессий по сфере и навыку."""

from __future__ import annotations



def filter_jobs(
    jobs: list[dict],
    sphere: str | None = None,
    skill: str | None = None,
) -> list[dict]:
    """
    Фильтрует список профессий по выбранной сфере и/или навыку.

    Args:
        jobs (list[dict]): Список карточек профессий.
        sphere (str | None): Значение сферы для фильтрации.
        skill (str | None): Значение навыка для фильтрации.

    Returns:
        list[dict]: Отфильтрованный список профессий.
    """
    filtered = jobs

    if sphere:
        filtered = [job for job in filtered if sphere in job.get("sphere", [])]

    if skill:
        filtered = [job for job in filtered if skill in job.get("skills", [])]

    return filtered


if __name__ == "__main__":
    from services.load_json_data import load_json_data

    jobs_data = load_json_data("new_jobs.json")
    result = filter_jobs(jobs_data, sphere="AI", skill="critical_thinking")
    print(f"Найдено профессий: {len(result)}")
