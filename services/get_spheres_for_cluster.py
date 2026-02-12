"""Получение списка сфер, входящих в выбранный кластер."""

from __future__ import annotations



def get_spheres_for_cluster(jobs: list[dict], cluster_name: str) -> list[str]:
    """
    Возвращает уникальные сферы для указанного кластера.

    Args:
        jobs (list[dict]): Список карточек профессий.
        cluster_name (str): Название выбранного кластера.

    Returns:
        list[str]: Отсортированный список сфер кластера.
    """
    cluster_spheres = {
        sphere
        for job in jobs
        if cluster_name in job.get("cluster", [])
        for sphere in job.get("sphere", [])
    }
    return sorted(cluster_spheres)


if __name__ == "__main__":
    from services.load_json_data import load_json_data

    jobs_data = load_json_data("new_jobs.json")
    result = get_spheres_for_cluster(jobs_data, "Цифровые и интеллектуальные технологии")
    print(f"Сфер в кластере: {len(result)}")
