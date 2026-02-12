"""Формирование топ-списка рекомендаций по профилю пользователя."""

from __future__ import annotations

from services.score_recommendation_job import score_recommendation_job



def get_recommended_jobs(
    jobs: list[dict],
    profile: dict[str, dict[str, int]],
    top_k: int = 10,
) -> list[dict]:
    """
    Возвращает лучшие профессии по рассчитанному score.

    Args:
        jobs (list[dict]): Список всех профессий.
        profile (dict[str, dict[str, int]]): Профиль пользователя.
        top_k (int): Количество рекомендаций в выдаче.

    Returns:
        list[dict]: Отсортированный список профессий с полями `score` и `explanation`.
    """
    scored_jobs = []

    for job in jobs:
        score, explanation = score_recommendation_job(job, profile)
        enriched_job = dict(job)
        enriched_job["score"] = score
        enriched_job["explanation"] = explanation
        scored_jobs.append(enriched_job)

    scored_jobs.sort(key=lambda item: (item.get("score", 0), item.get("rate", 0)), reverse=True)
    return scored_jobs[:top_k]


if __name__ == "__main__":
    sample_jobs = [
        {
            "id": 1,
            "title": "Инженер ИИ",
            "cluster": ["Цифровые и интеллектуальные технологии"],
            "activity": ["analysis", "development"],
            "skills": ["python"],
            "rate": 3,
        },
        {
            "id": 2,
            "title": "Экоаналитик",
            "cluster": ["Устойчивая среда и природные ресурсы"],
            "activity": ["research"],
            "skills": ["ecology_basics"],
            "rate": 1,
        },
    ]
    sample_profile = {
        "clusters": {"Цифровые и интеллектуальные технологии": 2},
        "activities": {"analysis": 1},
        "skills": {"python": 1},
    }
    result = get_recommended_jobs(sample_jobs, sample_profile, top_k=2)
    print([(item["title"], item["score"]) for item in result])
