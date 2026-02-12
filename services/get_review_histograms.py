"""Агрегация оценок отзывов для построения гистограмм."""

from __future__ import annotations


def get_review_histograms(
    grades_data: list[dict],
    questions: list[str],
    scale: list[dict],
) -> list[dict]:
    """
    Формирует данные гистограмм по вопросам отзывов.

    Args:
        grades_data (list[dict]): Список сохранённых отзывов из `grades.json`.
        questions (list[str]): Список текстов вопросов в фиксированном порядке.
        scale (list[dict]): Шкала оценок в формате `[{\"value\": 1, \"label\": \"...\"}, ...]`.

    Returns:
        list[dict]: Список гистограмм по вопросам с полями `question`, `total` и `bars`.
    """
    scale_values = [int(item.get("value", 0)) for item in scale]
    scale_labels = {int(item.get("value", 0)): item.get("label", "") for item in scale}

    histograms: list[dict] = []
    for index, question in enumerate(questions, start=1):
        question_id = f"q{index}"
        counts = {value: 0 for value in scale_values}

        for review in grades_data:
            raw_value = review.get("grades", {}).get(question_id)
            try:
                value = int(raw_value)
            except (TypeError, ValueError):
                continue
            if value in counts:
                counts[value] += 1

        total = sum(counts.values())
        bars = []
        for value in scale_values:
            count = counts[value]
            percent = round((count / total) * 100, 1) if total else 0.0
            bars.append(
                {
                    "value": value,
                    "label": scale_labels.get(value, ""),
                    "count": count,
                    "percent": percent,
                }
            )

        histograms.append(
            {
                "id": question_id,
                "question": question,
                "total": total,
                "bars": bars,
            }
        )

    return histograms


if __name__ == "__main__":
    sample_data = [
        {"grades": {"q1": 5, "q2": 4, "q3": 3}},
        {"grades": {"q1": 4, "q2": 4, "q3": 5}},
    ]
    sample_questions = [
        "Вопрос 1",
        "Вопрос 2",
        "Вопрос 3",
    ]
    sample_scale = [
        {"value": 1, "label": "нет"},
        {"value": 2, "label": "скорее нет"},
        {"value": 3, "label": "не знаю"},
        {"value": 4, "label": "скорее да"},
        {"value": 5, "label": "да"},
    ]
    print(get_review_histograms(sample_data, sample_questions, sample_scale)[0])
