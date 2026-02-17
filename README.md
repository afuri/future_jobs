# Каталог профессий будущего

Веб-приложение на Flask для навигации по профессиям будущего, фильтрации, рекомендаций, лайков и выгрузки PDF.

## Что реализовано

- Каталог профессий с иерархией:
  - кластеры -> сферы -> список профессий -> раскрытие карточки профессии
- Фильтры в верхнем меню:
  - по сфере
  - по навыку
- Страница `Топ профессий`:
  - топ-10 по `rate`
  - лайк профессии (сердце + счетчик) с возможностью снять лайк повторным нажатием
  - выгрузка списка в PDF
- Рекомендательный тест:
  - последовательные вопросы (следующий после ответа на предыдущий)
  - результаты: ТОП-3 + еще 7 профессий
  - объяснение совпадений и навыков для развития
  - выгрузка рекомендаций в PDF
- Форма `Добавить профессию`:
  - валидация обязательных полей
  - добавление пользовательской сферы и навыков
  - сохранение в `addition_jobs.json`


## Технологии

- Python
- Flask
- Jinja2
- HTML/CSS
- JSON как хранилище данных
- ReportLab (генерация PDF)

## Данные проекта

- `new_jobs.json` — основной каталог профессий
- `description.json` — переводы значений полей (`sphere`, `activity`, `skills`)
- `addition_jobs.json` — профессии, добавленные пользователями
- `clusters.md` — описание кластеров и связей

## Структура проекта

```text
future_jobs/
  main.py
  requirements.txt
  new_jobs.json
  description.json
  addition_jobs.json
  grades.json
  services/
    build_jobs_pdf_bytes.py
    filter_jobs.py
    get_filter_options.py
    get_top_jobs.py
    get_recommendation_questions.py
    build_recommendation_profile.py
    get_recommended_jobs.py
    score_recommendation_job.py
    translate_job_card.py
    save_addition_job_to_file.py
    increment_job_rate_in_file.py
    get_clusters_overview.py
    get_spheres_for_cluster.py
    load_json_data.py
    split_custom_values.py
  templates/
    index.html
    recommendation.html
    add_job.html
    internship_review.html
    review_stats.html
  static/
    style.css
    images/clusters/*.png
```

## Функции проекта

Краткое назначение функций из директории `services/`:

| Файл | Функция | Назначение |
|---|---|---|
| `services/load_json_data.py` | `load_json_data` | Загружает JSON из файла и возвращает `list` или `dict`. |
| `services/filter_jobs.py` | `filter_jobs` | Фильтрует профессии по сфере и/или навыку. |
| `services/get_filter_options.py` | `get_filter_options` | Собирает уникальные значения сфер и навыков для выпадающих списков. |
| `services/get_clusters_overview.py` | `get_clusters_overview` | Формирует карточки кластеров с описанием, логотипом и количеством профессий. |
| `services/get_spheres_for_cluster.py` | `get_spheres_for_cluster` | Возвращает список сфер, входящих в выбранный кластер. |
| `services/translate_job_card.py` | `translate_job_card` | Переводит коды полей профессии в русские подписи для UI. |
| `services/get_top_jobs.py` | `get_top_jobs` | Выбирает топ профессий по рейтингу `rate` с учетом ничьих на границе. |
| `services/increment_job_rate_in_file.py` | `increment_job_rate_in_file` | Увеличивает `rate` профессии в JSON по `job_id`. |
| `services/get_recommendation_questions.py` | `get_recommendation_questions` | Возвращает структуру вопросов и вариантов рекомендательного теста. |
| `services/build_recommendation_profile.py` | `build_recommendation_profile` | Преобразует ответы теста в профиль предпочтений пользователя (кластеры/активности/навыки). |
| `services/score_recommendation_job.py` | `score_recommendation_job` | Считает балл одной профессии по профилю и формирует объяснение совпадений. |
| `services/get_recommended_jobs.py` | `get_recommended_jobs` | Сортирует профессии по итоговому `score` и отдает топ рекомендаций. |
| `services/build_jobs_pdf_bytes.py` | `build_jobs_pdf_bytes` | Генерирует PDF-байты со списком профессий для скачивания. |
| `services/split_custom_values.py` | `split_custom_values` | Разбирает пользовательский ввод с разделителями в список уникальных значений. |
| `services/save_addition_job_to_file.py` | `save_addition_job_to_file` | Сохраняет новую профессию из формы в `addition_jobs.json`. |


## Маршруты

- `GET /` — главная страница каталога
- `POST /like/<job_id>` — лайк профессии
- `GET|POST /recommendation` — тест и рекомендации
- `GET /download-jobs-pdf` — скачивание PDF (`ids`, `source`)
- `GET|POST /add-job` — форма добавления профессии

