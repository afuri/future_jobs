"""Получение списка сфер, входящих в выбранный кластер."""

from __future__ import annotations

from pathlib import Path


def get_spheres_for_cluster(
    jobs: list[dict],
    cluster_name: str,
    clusters_file_path: str = "clusters.md",
) -> list[str]:
    """
    Возвращает сферы кластера по закреплению из `clusters.md`.

    Логика:
    1. Читает `clusters.md` и извлекает связи `сфера -> кластер` по markdown-разделам.
    2. Оставляет только сферы выбранного кластера.
    3. Пересекает их со сферами, реально присутствующими в `jobs`.

    Это гарантирует, что одна сфера отображается только у "своего" кластера.

    Args:
        jobs (list[dict]): Список карточек профессий.
        cluster_name (str): Название выбранного кластера.
        clusters_file_path (str): Путь до файла `clusters.md`.

    Returns:
        list[str]: Список сфер кластера в порядке из `clusters.md`.
    """
    file_path = Path(clusters_file_path)
    if not file_path.exists():
        return []

    lines = file_path.read_text(encoding="utf-8").splitlines()

    current_cluster = ""
    ordered_spheres: list[str] = []
    owner_by_sphere: dict[str, str] = {}

    for raw_line in lines:
        line = raw_line.strip()
        if not line:
            continue

        if line.startswith("## "):
            header = line[3:].strip()
            if ". " in header:
                current_cluster = header.split(". ", 1)[1].strip()
            else:
                current_cluster = header
            continue

        if "—" in line and current_cluster and not line.startswith("Фокус"):
            sphere_code = line.split("—", 1)[0].strip()
            if not sphere_code:
                continue
            if sphere_code not in owner_by_sphere:
                owner_by_sphere[sphere_code] = current_cluster
                ordered_spheres.append(sphere_code)

    existing_spheres = {
        sphere
        for job in jobs
        for sphere in job.get("sphere", [])
    }

    return [
        sphere
        for sphere in ordered_spheres
        if owner_by_sphere.get(sphere) == cluster_name and sphere in existing_spheres
    ]


if __name__ == "__main__":
    from services.load_json_data import load_json_data

    jobs_data = load_json_data("new_jobs.json")
    result = get_spheres_for_cluster(
        jobs_data,
        "Цифровые и интеллектуальные технологии",
        "clusters.md",
    )
    print(f"Сфер в кластере: {len(result)}")
