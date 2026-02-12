"""Формирование профиля пользователя по ответам теста."""

from __future__ import annotations

from collections import defaultdict


CLUSTER_DIGITAL = "Цифровые и интеллектуальные технологии"
CLUSTER_SCIENCE = "Наука, медицина и новые материалы"
CLUSTER_SUSTAINABLE = "Устойчивая среда и природные ресурсы"
CLUSTER_INFRA = "Инфраструктура, транспорт и промышленность"
CLUSTER_ECONOMY = "Экономика, управление и рынок труда"
CLUSTER_HUMAN = "Человек, общество и креативные индустрии"

ANSWER_EFFECTS = {
    "q1": {
        "A": {
            "clusters": [CLUSTER_DIGITAL],
            "activities": ["analysis"],
            "skills": ["data_analysis", "critical_thinking"],
        },
        "B": {
            "clusters": [CLUSTER_HUMAN],
            "activities": ["design", "creativity"],
            "skills": ["creativity", "ux_design"],
        },
        "C": {
            "clusters": [CLUSTER_HUMAN],
            "activities": ["communication", "consulting"],
            "skills": ["communication", "empathy"],
        },
        "D": {
            "clusters": [CLUSTER_INFRA],
            "activities": ["engineering", "design"],
            "skills": ["systems_thinking", "structural_thinking"],
        },
        "E": {
            "clusters": [CLUSTER_DIGITAL],
            "activities": ["analysis", "engineering"],
            "skills": ["systems_thinking", "problem_solving"],
        },
    },
    "q2": {
        "A": {
            "clusters": [CLUSTER_DIGITAL],
            "activities": ["development"],
            "skills": ["digital_literacy", "systems_thinking"],
        },
        "B": {
            "clusters": [CLUSTER_SCIENCE],
            "activities": ["research"],
            "skills": ["experiment_control", "critical_thinking"],
        },
        "C": {
            "clusters": [CLUSTER_SUSTAINABLE],
            "activities": ["research", "fieldwork"],
            "skills": ["ecology_basics", "field_observation"],
        },
        "D": {
            "clusters": [CLUSTER_ECONOMY],
            "activities": ["management", "planning"],
            "skills": ["planning", "organization"],
        },
        "E": {
            "clusters": [CLUSTER_HUMAN],
            "activities": ["communication"],
            "skills": ["cultural_analysis", "communication"],
        },
    },
    "q3": {
        "A": {
            "clusters": [CLUSTER_DIGITAL],
            "activities": ["development", "analysis"],
            "skills": ["python", "data_literacy"],
        },
        "B": {
            "clusters": [CLUSTER_SCIENCE],
            "activities": ["research"],
            "skills": ["biology_basics", "public_health"],
        },
        "C": {
            "clusters": [CLUSTER_INFRA],
            "activities": ["design", "planning"],
            "skills": ["systems_thinking", "spatial_thinking"],
        },
        "D": {
            "clusters": [CLUSTER_ECONOMY],
            "activities": ["management"],
            "skills": ["project_management", "planning"],
        },
        "E": {
            "clusters": [CLUSTER_HUMAN],
            "activities": ["creativity", "design"],
            "skills": ["creativity", "content_analysis"],
        },
    },
    "q4": {
        "A": {
            "clusters": [CLUSTER_DIGITAL],
            "activities": ["operations"],
            "skills": ["stress_resilience", "problem_solving"],
        },
        "B": {
            "clusters": [CLUSTER_ECONOMY],
            "activities": ["operations"],
            "skills": ["organization", "process_control"],
        },
        "C": {
            "clusters": [CLUSTER_SCIENCE],
            "activities": ["research"],
            "skills": ["critical_thinking", "trend_analysis"],
        },
        "D": {
            "clusters": [CLUSTER_ECONOMY],
            "activities": ["management", "policy"],
            "skills": ["decision_making", "negotiation"],
        },
        "E": {
            "clusters": [CLUSTER_HUMAN],
            "activities": ["consulting", "communication"],
            "skills": ["empathy", "public_health"],
        },
    },
    "q5": {
        "A": {
            "clusters": [CLUSTER_DIGITAL],
            "activities": ["development"],
            "skills": ["python", "digital_literacy"],
        },
        "B": {
            "clusters": [CLUSTER_SCIENCE],
            "activities": ["analysis"],
            "skills": ["critical_thinking", "systems_thinking"],
        },
        "C": {
            "clusters": [CLUSTER_HUMAN],
            "activities": ["communication"],
            "skills": ["communication", "empathy"],
        },
        "D": {
            "clusters": [CLUSTER_ECONOMY],
            "activities": ["management"],
            "skills": ["project_management", "organization"],
        },
        "E": {
            "clusters": [CLUSTER_HUMAN],
            "activities": ["design"],
            "skills": ["ux_design", "creativity"],
        },
    },
    "q6": {
        "A": {
            "clusters": [CLUSTER_DIGITAL],
            "activities": ["analysis", "development"],
            "skills": ["digital_literacy", "data_analysis"],
        },
        "B": {
            "clusters": [CLUSTER_HUMAN],
            "activities": ["communication", "management"],
            "skills": ["teamwork", "communication"],
        },
        "C": {
            "clusters": [CLUSTER_SCIENCE],
            "activities": ["research"],
            "skills": ["critical_thinking", "experiment_control"],
        },
        "D": {
            "clusters": [CLUSTER_ECONOMY, CLUSTER_INFRA],
            "activities": ["operations", "management"],
            "skills": ["process_control", "planning"],
        },
        "E": {
            "clusters": [CLUSTER_INFRA, CLUSTER_HUMAN],
            "activities": ["design", "development"],
            "skills": ["product_thinking", "creativity"],
        },
    },
    "q7": {
        "A": {
            "clusters": [CLUSTER_DIGITAL],
            "activities": ["development"],
            "skills": ["innovation", "systems_thinking"],
        },
        "B": {
            "clusters": [CLUSTER_HUMAN, CLUSTER_SCIENCE],
            "activities": ["consulting", "communication"],
            "skills": ["empathy", "public_health"],
        },
        "C": {
            "clusters": [CLUSTER_SUSTAINABLE],
            "activities": ["planning", "research"],
            "skills": ["ecology_basics", "life_cycle_thinking"],
        },
        "D": {
            "clusters": [CLUSTER_ECONOMY],
            "activities": ["management", "analysis"],
            "skills": ["planning", "data_analysis"],
        },
        "E": {
            "clusters": [CLUSTER_HUMAN],
            "activities": ["creativity", "communication"],
            "skills": ["cultural_analysis", "creativity"],
        },
    },
}


def build_recommendation_profile(answers: dict[str, str]) -> dict[str, dict[str, int]]:
    """
    Формирует профиль пользователя по ответам теста.

    Args:
        answers (dict[str, str]): Ответы пользователя в формате `{"q1": "A", ...}`.

    Returns:
        dict[str, dict[str, int]]: Словарь счётчиков по кластерам, видам деятельности и навыкам.
    """
    profile = {
        "clusters": defaultdict(int),
        "activities": defaultdict(int),
        "skills": defaultdict(int),
    }

    for question_id, answer_code in answers.items():
        option_effect = ANSWER_EFFECTS.get(question_id, {}).get(answer_code)
        if not option_effect:
            continue

        for cluster in option_effect.get("clusters", []):
            profile["clusters"][cluster] += 1
        for activity in option_effect.get("activities", []):
            profile["activities"][activity] += 1
        for skill in option_effect.get("skills", []):
            profile["skills"][skill] += 1

    return {
        "clusters": dict(profile["clusters"]),
        "activities": dict(profile["activities"]),
        "skills": dict(profile["skills"]),
    }


if __name__ == "__main__":
    sample_answers = {"q1": "A", "q2": "A", "q3": "A", "q4": "C", "q5": "A", "q6": "A", "q7": "A"}
    sample_profile = build_recommendation_profile(sample_answers)
    print(sample_profile)
