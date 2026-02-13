"""Получение топ-профессий по полю rate."""

from __future__ import annotations

import random



def get_top_jobs(jobs: list[dict], top_k: int = 10) -> list[dict]:
    """
    Возвращает список топ-профессий по рейтингу `rate`.

    Если на пограничном значении рейтинга кандидатов больше, чем оставшихся
    мест в выдаче, выбираются случайные профессии из этой группы.

    Args:
        jobs (list[dict]): Список карточек профессий.
        top_k (int): Максимальное количество профессий в выдаче.

    Returns:
        list[dict]: Список профессий, упорядоченный по `rate` по убыванию.
    """
    if not jobs or top_k <= 0:
        return []

    grouped_by_rate: dict[int, list[dict]] = {}
    for job in jobs:
        grouped_by_rate.setdefault(int(job.get("rate", 0)), []).append(job)

    selected: list[dict] = []
    for rate in sorted(grouped_by_rate.keys(), reverse=True):
        group = grouped_by_rate[rate]
        remaining_slots = top_k - len(selected)
        if remaining_slots <= 0:
            break

        if len(group) <= remaining_slots:
            selected.extend(sorted(group, key=lambda item: item.get("title", "")))
            continue

        selected.extend(random.sample(group, remaining_slots))
        break
    
    return selected


if __name__ == "__main__":
    from services.load_json_data import load_json_data

    jobs_data = load_json_data("new_jobs.json")
    top = get_top_jobs(jobs_data, top_k=10)
    print(f"Выдано профессий: {len(top)}")
