"""Подготовка карточек кластеров для главной страницы."""

from __future__ import annotations



def get_clusters_overview(
    jobs: list[dict],
    cluster_descriptions: dict[str, str],
    cluster_logos: dict[str, str],
) -> list[dict]:
    """
    Формирует список кластеров с метаданными и набором сфер.

    Args:
        jobs (list[dict]): Список карточек профессий.
        cluster_descriptions (dict[str, str]): Краткие описания кластеров.
        cluster_logos (dict[str, str]): Относительные пути до логотипов кластеров.

    Returns:
        list[dict]: Список словарей с данными по кластерам для отображения.
    """
    clusters: dict[str, dict] = {}

    for job in jobs:
        for cluster_name in job.get("cluster", []):
            if cluster_name not in clusters:
                clusters[cluster_name] = {
                    "name": cluster_name,
                    "logo": cluster_logos.get(cluster_name, ""),
                    "description": cluster_descriptions.get(
                        cluster_name,
                        "Кластер профессий будущего.",
                    ),
                    "spheres": set(),
                    "jobs_count": 0,
                }
            clusters[cluster_name]["jobs_count"] += 1
            clusters[cluster_name]["spheres"].update(job.get("sphere", []))

    normalized = []
    for cluster in clusters.values():
        cluster["spheres"] = sorted(cluster["spheres"])
        normalized.append(cluster)

    return sorted(normalized, key=lambda item: item["name"])


if __name__ == "__main__":
    from services.load_json_data import load_json_data

    jobs_data = load_json_data("new_jobs.json")
    overview = get_clusters_overview(jobs_data, {}, {})
    print(f"Кластеров: {len(overview)}")
