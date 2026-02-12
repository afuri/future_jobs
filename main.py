"""Flask-приложение каталога профессий будущего."""

from __future__ import annotations

import os
from pathlib import Path

from flask import Flask, redirect, render_template, request, session, url_for

from services.build_recommendation_profile import build_recommendation_profile
from services.filter_jobs import filter_jobs
from services.get_clusters_overview import get_clusters_overview
from services.get_filter_options import get_filter_options
from services.get_recommendation_questions import get_recommendation_questions
from services.get_recommended_jobs import get_recommended_jobs
from services.get_review_histograms import get_review_histograms
from services.get_spheres_for_cluster import get_spheres_for_cluster
from services.get_top_jobs import get_top_jobs
from services.increment_job_rate_in_file import increment_job_rate_in_file
from services.load_json_data import load_json_data
from services.save_addition_job_to_file import save_addition_job_to_file
from services.save_review_grades_to_file import save_review_grades_to_file
from services.split_custom_values import split_custom_values
from services.translate_job_card import translate_job_card

BASE_DIR = Path(__file__).resolve().parent
JOBS_PATH = BASE_DIR / "new_jobs.json"
DESCRIPTION_PATH = BASE_DIR / "description.json"
ADDITION_JOBS_PATH = BASE_DIR / "addition_jobs.json"
GRADES_PATH = BASE_DIR / "grades.json"

APP_TITLE = "Каталог Профессий Будущего"

INTERNSHIP_REVIEW_QUESTIONS = [
    "Я понял принцип модульного построения программ",
    "Мне понравилось работать над web-приложением",
    "Я положу данный проект а свое портфолио",
]

INTERNSHIP_REVIEW_SCALE = [
    {"value": 1, "label": "нет"},
    {"value": 2, "label": "скорее нет"},
    {"value": 3, "label": "не знаю"},
    {"value": 4, "label": "скорее да"},
    {"value": 5, "label": "да"},
]

CLUSTER_DESCRIPTIONS = {
    "Цифровые и интеллектуальные технологии": (
        "Алгоритмы, данные, автоматизация и цифровая инфраструктура."
    ),
    "Наука, медицина и новые материалы": (
        "Исследования, биотехнологии, медицина и инженерия материалов."
    ),
    "Устойчивая среда и природные ресурсы": (
        "Экология, энергетика и рациональное управление природными ресурсами."
    ),
    "Инфраструктура, транспорт и промышленность": (
        "Города, производство, транспортные системы и космические решения."
    ),
    "Экономика, управление и рынок труда": (
        "Финансы, управленческие модели и новые механики рынка труда."
    ),
    "Человек, общество и креативные индустрии": (
        "Образование, коммуникации, культура и социальные процессы."
    ),
}

CLUSTER_LOGOS = {
    "Цифровые и интеллектуальные технологии": "images/clusters/ai.png",
    "Наука, медицина и новые материалы": "images/clusters/medicine.png",
    "Устойчивая среда и природные ресурсы": "images/clusters/ecology.png",
    "Инфраструктура, транспорт и промышленность": "images/clusters/transport.png",
    "Экономика, управление и рынок труда": "images/clusters/economy.png",
    "Человек, общество и креативные индустрии": "images/clusters/human.png",
}

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "future-jobs-dev-key")


def build_url_params(**kwargs: str | None) -> dict[str, str]:
    """
    Формирует словарь query-параметров без пустых значений.

    Args:
        **kwargs (str | None): Пары ключ-значение параметров URL.

    Returns:
        dict[str, str]: Параметры для передачи в `url_for`.
    """
    return {key: value for key, value in kwargs.items() if value}


def parse_liked_job_ids(raw_values: list) -> set[int]:
    """
    Преобразует список значений из сессии в множество корректных `job_id`.

    Args:
        raw_values (list): Сырые значения из `session`.

    Returns:
        set[int]: Множество валидных целочисленных идентификаторов.
    """
    parsed: set[int] = set()
    for value in raw_values:
        try:
            parsed.add(int(value))
        except (TypeError, ValueError):
            continue
    return parsed


def get_sorted_profile_skills(profile: dict[str, dict[str, int]]) -> list[str]:
    """
    Возвращает навыки профиля в порядке убывания релевантности.

    Args:
        profile (dict[str, dict[str, int]]): Профиль пользователя.

    Returns:
        list[str]: Список кодов навыков, отсортированный по весу.
    """
    weighted_skills = profile.get("skills", {})
    sorted_items = sorted(
        weighted_skills.items(),
        key=lambda item: (item[1], item[0]),
        reverse=True,
    )
    return [skill for skill, _ in sorted_items]


def build_recommendation_card(
    job: dict,
    description_data: dict,
    profile_skill_order: list[str],
) -> dict:
    """
    Формирует локализованную карточку рекомендации с пояснениями.

    Args:
        job (dict): Профессия с полями `score` и `explanation`.
        description_data (dict): Словарь переводов.
        profile_skill_order (list[str]): Навыки профиля по убыванию веса.

    Returns:
        dict: Готовая карточка для отображения в шаблоне.
    """
    activity_map = description_data.get("activity", {})
    skills_map = description_data.get("skills", {})

    translated = translate_job_card(job, description_data)
    explanation = job.get("explanation", {})
    job_skill_codes = set(job.get("skills", []))

    matched_activities = [
        activity_map.get(code, code)
        for code in explanation.get("matched_activities", [])
    ]
    matched_skills = [
        skills_map.get(code, code)
        for code in explanation.get("matched_skills", [])
    ]
    development_skills = [
        skills_map.get(code, code)
        for code in profile_skill_order
        if code not in job_skill_codes
    ][:3]

    translated["score"] = int(job.get("score", 0))
    translated["matched_activities"] = matched_activities
    translated["matched_skills"] = matched_skills
    translated["development_skills"] = development_skills
    translated["matched_clusters"] = explanation.get("matched_clusters", [])
    return translated


def merge_unique_values(values: list[str]) -> list[str]:
    """
    Удаляет дубликаты с сохранением исходного порядка.

    Args:
        values (list[str]): Исходный список значений.

    Returns:
        list[str]: Уникальные значения в порядке появления.
    """
    unique_values: list[str] = []
    seen: set[str] = set()
    for value in values:
        normalized = value.strip()
        if not normalized:
            continue
        marker = normalized.casefold()
        if marker in seen:
            continue
        seen.add(marker)
        unique_values.append(normalized)
    return unique_values


@app.route("/")
def index() -> str:
    """Отображает главную страницу каталога с фильтрами и карточками профессий."""
    jobs_data = load_json_data(str(JOBS_PATH))
    description_data = load_json_data(str(DESCRIPTION_PATH))

    selected_cluster = request.args.get("cluster", "").strip() or None
    selected_sphere = request.args.get("sphere", "").strip() or None
    selected_skill = request.args.get("skill", "").strip() or None
    view_mode = request.args.get("view", "").strip()
    top_ids_raw = request.args.get("top_ids", "").strip()

    open_job_raw = request.args.get("open", "").strip()
    open_job_id = int(open_job_raw) if open_job_raw.isdigit() else None

    liked_job_ids = parse_liked_job_ids(session.get("liked_jobs", []))

    filter_options = get_filter_options(jobs_data)

    sphere_options = [
        {
            "value": value,
            "label": description_data.get("sphere", {}).get(value, value),
        }
        for value in filter_options["sphere"]
    ]
    skill_options = [
        {
            "value": value,
            "label": description_data.get("skills", {}).get(value, value),
        }
        for value in filter_options["skills"]
    ]

    cluster_cards = get_clusters_overview(
        jobs_data,
        cluster_descriptions=CLUSTER_DESCRIPTIONS,
        cluster_logos=CLUSTER_LOGOS,
    )

    spheres_for_cluster = (
        get_spheres_for_cluster(jobs_data, selected_cluster) if selected_cluster else []
    )
    sphere_cards = [
        {
            "value": sphere,
            "label": description_data.get("sphere", {}).get(sphere, sphere),
        }
        for sphere in spheres_for_cluster
    ]

    result_jobs: list[dict]
    result_title = ""
    top_ids_param: str | None = None

    if view_mode == "top":
        top_ids = []
        if top_ids_raw:
            for value in top_ids_raw.split(","):
                value = value.strip()
                if value.isdigit():
                    top_ids.append(int(value))

        jobs_by_id = {int(job.get("id", 0)): job for job in jobs_data}
        preserved_top = [jobs_by_id[job_id] for job_id in top_ids if job_id in jobs_by_id]

        if preserved_top:
            result_jobs = preserved_top[:10]
        else:
            result_jobs = get_top_jobs(jobs_data, top_k=10)

        top_ids_param = ",".join(str(int(job.get("id", 0))) for job in result_jobs)
        result_title = "Топ профессий"
    elif selected_sphere or selected_skill:
        filtered_jobs = filter_jobs(
            jobs_data,
            sphere=selected_sphere,
            skill=selected_skill,
        )
        result_jobs = sorted(filtered_jobs, key=lambda item: item.get("title", ""))
        result_title = "Результаты фильтрации"
    else:
        result_jobs = []

    translated_jobs = [
        translate_job_card(job, description_data)
        for job in result_jobs
    ]

    show_clusters_section = (
        not selected_cluster
        and not selected_sphere
        and not selected_skill
        and view_mode != "top"
    )
    show_spheres_section = (
        bool(selected_cluster)
        and not selected_sphere
        and not selected_skill
        and view_mode != "top"
    )

    sphere_label = (
        description_data.get("sphere", {}).get(selected_sphere, selected_sphere)
        if selected_sphere
        else None
    )
    skill_label = (
        description_data.get("skills", {}).get(selected_skill, selected_skill)
        if selected_skill
        else None
    )

    breadcrumbs: list[dict[str, str | None]] = [
        {"label": "Главная", "url": url_for("index")}
    ]
    if view_mode == "top":
        breadcrumbs.append({"label": "Топ профессий", "url": None})
    else:
        if selected_cluster:
            breadcrumbs.append(
                {
                    "label": selected_cluster,
                    "url": (
                        url_for("index", **build_url_params(cluster=selected_cluster))
                        if selected_sphere or selected_skill or open_job_id
                        else None
                    ),
                }
            )
        if selected_sphere:
            breadcrumbs.append(
                {
                    "label": f"Сфера: {sphere_label}",
                    "url": (
                        url_for(
                            "index",
                            **build_url_params(
                                cluster=selected_cluster,
                                sphere=selected_sphere,
                            ),
                        )
                        if selected_skill or open_job_id
                        else None
                    ),
                }
            )
        if selected_skill:
            breadcrumbs.append({"label": f"Навык: {skill_label}", "url": None})
        if open_job_id:
            breadcrumbs.append({"label": "Карточка профессии", "url": None})

    back_url: str | None = None
    back_label: str = "Назад"
    if open_job_id:
        back_url = url_for(
            "index",
            **build_url_params(
                cluster=selected_cluster,
                sphere=selected_sphere,
                skill=selected_skill,
                view=view_mode,
                top_ids=top_ids_param,
            ),
        )
        back_label = "Назад к списку"
    elif selected_sphere:
        back_url = url_for("index", **build_url_params(cluster=selected_cluster))
        back_label = "Назад к выбору сфер"
    elif selected_cluster:
        back_url = url_for("index")
        back_label = "Назад к кластерам"
    elif selected_skill or view_mode == "top":
        back_url = url_for("index")
        back_label = "Назад к выбору"

    return render_template(
        "index.html",
        app_title=APP_TITLE,
        sphere_options=sphere_options,
        skill_options=skill_options,
        selected_sphere=selected_sphere,
        selected_skill=selected_skill,
        selected_cluster=selected_cluster,
        cluster_cards=cluster_cards,
        sphere_cards=sphere_cards,
        jobs=translated_jobs,
        result_title=result_title,
        view_mode=view_mode,
        top_ids_param=top_ids_param,
        open_job_id=open_job_id,
        liked_job_ids=liked_job_ids,
        show_clusters_section=show_clusters_section,
        show_spheres_section=show_spheres_section,
        breadcrumbs=breadcrumbs,
        back_url=back_url,
        back_label=back_label,
    )


@app.route("/recommendation", methods=["GET", "POST"])
def recommendation() -> str:
    """
    Отображает и обрабатывает рекомендательный тест профессий.

    Args:
        Нет.

    Returns:
        str: HTML-страница теста и результатов рекомендаций.
    """
    jobs_data = load_json_data(str(JOBS_PATH))
    description_data = load_json_data(str(DESCRIPTION_PATH))
    questions = get_recommendation_questions()

    answers: dict[str, str] = {}
    validation_error: str | None = None
    top_jobs: list[dict] = []
    additional_jobs: list[dict] = []
    recommendations_ready = False

    if request.method == "POST":
        for question in questions:
            question_id = question.get("id", "")
            answer = request.form.get(question_id, "").strip().upper()
            if answer in question.get("options", {}):
                answers[question_id] = answer

        if len(answers) != len(questions):
            validation_error = "Ответьте на все 7 вопросов теста."
        else:
            recommendations_ready = True
            profile = build_recommendation_profile(answers)
            profile_skill_order = get_sorted_profile_skills(profile)
            recommended_jobs = get_recommended_jobs(jobs_data, profile, top_k=10)

            translated_recommended = [
                build_recommendation_card(job, description_data, profile_skill_order)
                for job in recommended_jobs
            ]
            top_jobs = translated_recommended[:3]
            additional_jobs = translated_recommended[3:10]

    return render_template(
        "recommendation.html",
        app_title=APP_TITLE,
        questions=questions,
        answers=answers,
        validation_error=validation_error,
        top_jobs=top_jobs,
        additional_jobs=additional_jobs,
        recommendations_ready=recommendations_ready,
    )


@app.route("/add-job", methods=["GET", "POST"])
def add_job() -> str:
    """
    Отображает форму добавления профессии и сохраняет пользовательские данные.

    Args:
        Нет.

    Returns:
        str: HTML-страница формы добавления профессии.
    """
    jobs_data = load_json_data(str(JOBS_PATH))
    description_data = load_json_data(str(DESCRIPTION_PATH))
    filter_options = get_filter_options(jobs_data)

    sphere_options = [
        {
            "value": value,
            "label": description_data.get("sphere", {}).get(value, value),
        }
        for value in filter_options["sphere"]
    ]
    skill_options = [
        {
            "value": value,
            "label": description_data.get("skills", {}).get(value, value),
        }
        for value in filter_options["skills"]
    ]

    form_data = {
        "title": "",
        "sphere_selected": "",
        "sphere_custom": "",
        "skills_selected": [],
        "skills_custom": "",
        "why_future": "",
        "tasks_text": "",
    }
    errors: list[str] = []

    if request.method == "POST":
        form_data["title"] = request.form.get("title", "").strip()
        form_data["sphere_selected"] = request.form.get("sphere_selected", "").strip()
        form_data["sphere_custom"] = request.form.get("sphere_custom", "").strip()
        form_data["skills_selected"] = [
            value.strip()
            for value in request.form.getlist("skills_selected")
            if value.strip()
        ]
        form_data["skills_custom"] = request.form.get("skills_custom", "").strip()
        form_data["why_future"] = request.form.get("why_future", "").strip()
        form_data["tasks_text"] = request.form.get("tasks_text", "").strip()

        sphere_values = merge_unique_values(
            [
                form_data["sphere_selected"],
                *split_custom_values(form_data["sphere_custom"]),
            ]
        )
        skill_values = merge_unique_values(
            [
                *form_data["skills_selected"],
                *split_custom_values(form_data["skills_custom"]),
            ]
        )
        tasks_values = split_custom_values(form_data["tasks_text"])

        if not form_data["title"]:
            errors.append("Укажите название профессии.")
        if not sphere_values:
            errors.append("Выберите сферу или добавьте свою.")
        if not skill_values:
            errors.append("Выберите хотя бы один навык или добавьте свой.")

        if not errors:
            save_addition_job_to_file(
                file_path=str(ADDITION_JOBS_PATH),
                title=form_data["title"],
                spheres=sphere_values,
                skills=skill_values,
                why_future=form_data["why_future"],
                tasks=tasks_values,
            )
            return redirect(url_for("add_job", saved="1"))

    is_saved = request.args.get("saved", "").strip() == "1"

    return render_template(
        "add_job.html",
        app_title=APP_TITLE,
        sphere_options=sphere_options,
        skill_options=skill_options,
        form_data=form_data,
        errors=errors,
        is_saved=is_saved,
    )


@app.route("/internship-review", methods=["GET", "POST"])
def internship_review() -> str:
    """
    Отображает страницу с формой отзыва о стажировке.

    Args:
        Нет.

    Returns:
        str: HTML-страница с вопросами и шкалой оценок.
    """
    review_questions = [
        {"id": f"q{index}", "text": question}
        for index, question in enumerate(INTERNSHIP_REVIEW_QUESTIONS, start=1)
    ]
    selected_values: dict[str, int] = {}
    errors: list[str] = []
    submitted_in_session = bool(session.get("internship_review_submitted", False))
    success_message: str | None = None

    if request.method == "POST":
        if submitted_in_session:
            errors.append("В рамках текущей сессии отзыв уже был отправлен.")
        else:
            for question in review_questions:
                raw_value = request.form.get(question["id"], "").strip()
                if raw_value in {"1", "2", "3", "4", "5"}:
                    selected_values[question["id"]] = int(raw_value)

            if len(selected_values) != len(review_questions):
                errors.append("Выберите оценку для каждого вопроса.")
            else:
                save_review_grades_to_file(
                    file_path=str(GRADES_PATH),
                    grades=selected_values,
                )
                session["internship_review_submitted"] = True
                submitted_in_session = True
                success_message = "Отзыв успешно отправлен."

    return render_template(
        "internship_review.html",
        app_title=APP_TITLE,
        questions=review_questions,
        rating_scale=INTERNSHIP_REVIEW_SCALE,
        selected_values=selected_values,
        errors=errors,
        submitted_in_session=submitted_in_session,
        success_message=success_message,
    )


@app.route("/review/")
def review_stats() -> str:
    """
    Отображает сводные гистограммы оценок по вопросам отзыва.

    Args:
        Нет.

    Returns:
        str: HTML-страница с тремя гистограммами.
    """
    grades_data: list[dict] = []
    if GRADES_PATH.exists():
        try:
            loaded = load_json_data(str(GRADES_PATH))
            if isinstance(loaded, list):
                grades_data = loaded
        except Exception:
            grades_data = []

    review_scale_desc = sorted(
        INTERNSHIP_REVIEW_SCALE,
        key=lambda item: int(item.get("value", 0)),
        reverse=True,
    )

    histograms = get_review_histograms(
        grades_data=grades_data,
        questions=INTERNSHIP_REVIEW_QUESTIONS,
        scale=review_scale_desc,
    )

    return render_template(
        "review_stats.html",
        app_title=APP_TITLE,
        histograms=histograms,
        total_reviews=len(grades_data),
    )


@app.post("/like/<int:job_id>")
def like_job(job_id: int):
    """
    Увеличивает число лайков у профессии и возвращает пользователя обратно.

    Args:
        job_id (int): Идентификатор профессии.

    Returns:
        Response: Редирект обратно на текущий экран каталога.
    """
    liked_job_ids = parse_liked_job_ids(session.get("liked_jobs", []))
    if job_id not in liked_job_ids:
        was_updated = increment_job_rate_in_file(str(JOBS_PATH), job_id)
        if was_updated:
            liked_job_ids.add(job_id)
            session["liked_jobs"] = sorted(liked_job_ids)

    selected_cluster = request.form.get("cluster", "").strip() or None
    selected_sphere = request.form.get("sphere", "").strip() or None
    selected_skill = request.form.get("skill", "").strip() or None
    view_mode = request.form.get("view", "").strip() or None
    open_job = request.form.get("open", "").strip() or None
    top_ids = request.form.get("top_ids", "").strip() or None

    return redirect(
        url_for(
            "index",
            **build_url_params(
                cluster=selected_cluster,
                sphere=selected_sphere,
                skill=selected_skill,
                view=view_mode,
                open=open_job,
                top_ids=top_ids,
            ),
        )
    )


if __name__ == "__main__":
    app.run(debug=True)
