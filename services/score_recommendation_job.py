"""Скоринг одной профессии по профилю пользователя."""

from __future__ import annotations



def score_recommendation_job(
    job: dict,
    profile: dict[str, dict[str, int]],
) -> tuple[int, dict[str, list[str] | int]]:
    """
    Вычисляет оценку профессии и формирует пояснение по совпадениям.

    Args:
        job (dict): Карточка профессии.
        profile (dict[str, dict[str, int]]): Профиль пользователя с весами по осям.

    Returns:
        tuple[int, dict[str, list[str] | int]]: Числовой score и словарь объяснения.
    """
    matched_clusters = [
        cluster for cluster in job.get("cluster", []) if cluster in profile.get("clusters", {})
    ]
    matched_activities = [
        activity
        for activity in job.get("activity", [])
        if activity in profile.get("activities", {})
    ]
    matched_skills = [
        skill for skill in job.get("skills", []) if skill in profile.get("skills", {})
    ]

    cluster_score = sum(profile["clusters"].get(cluster, 0) for cluster in matched_clusters)
    activity_score = sum(
        profile["activities"].get(activity, 0) for activity in matched_activities
    )
    skill_score = sum(profile["skills"].get(skill, 0) for skill in matched_skills)

    total_score = cluster_score * 50 + activity_score * 20 + skill_score * 10

    return total_score, {
        "matched_clusters": matched_clusters,
        "matched_activities": matched_activities,
        "matched_skills": matched_skills,
        "cluster_score": cluster_score,
        "activity_score": activity_score,
        "skill_score": skill_score,
    }


if __name__ == "__main__":
    sample_job = {
        "cluster": ["Цифровые и интеллектуальные технологии"],
        "activity": ["analysis", "development"],
        "skills": ["python", "data_analysis"],
    }
    sample_profile = {
        "clusters": {"Цифровые и интеллектуальные технологии": 2},
        "activities": {"analysis": 1},
        "skills": {"python": 2, "data_analysis": 1},
    }
    print(score_recommendation_job(sample_job, sample_profile))
