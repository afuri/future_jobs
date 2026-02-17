"""Генерация PDF-документа со списком карточек профессий."""

from __future__ import annotations

from datetime import datetime
from io import BytesIO
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


def build_jobs_pdf_bytes(jobs: list[dict], document_title: str) -> bytes:
    """
    Формирует PDF-байты со списком профессий.

    Args:
        jobs (list[dict]): Список карточек профессий для экспорта.
        document_title (str): Заголовок документа в PDF.

    Returns:
        bytes: Содержимое PDF-файла в байтах.
    """
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)

    font_name = "Helvetica"
    font_candidates = [
        ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "DejaVuSans"),
        ("/usr/share/fonts/dejavu/DejaVuSans.ttf", "DejaVuSans"),
        ("/System/Library/Fonts/Supplemental/Arial Unicode.ttf", "ArialUnicode"),
    ]
    for font_path, custom_name in font_candidates:
        if Path(font_path).exists():
            pdfmetrics.registerFont(TTFont(custom_name, font_path))
            font_name = custom_name
            break

    page_width, page_height = A4
    left_margin = 40
    right_margin = 40
    top_margin = page_height - 50
    bottom_margin = 50
    line_height = 14
    max_chars = 96

    def draw_line(text: str, size: int = 11, extra_gap: int = 0) -> float:
        nonlocal top_margin
        sanitized = (text or "").strip()
        if not sanitized:
            top_margin -= line_height + extra_gap
            return top_margin

        words = sanitized.split()
        lines: list[str] = []
        current = ""
        for word in words:
            candidate = f"{current} {word}".strip()
            if len(candidate) <= max_chars:
                current = candidate
            else:
                if current:
                    lines.append(current)
                current = word
        if current:
            lines.append(current)

        for line in lines:
            if top_margin < bottom_margin:
                pdf.showPage()
                pdf.setFont(font_name, size)
                top_margin = page_height - 50
            pdf.setFont(font_name, size)
            pdf.drawString(left_margin, top_margin, line)
            top_margin -= line_height

        top_margin -= extra_gap
        return top_margin

    now_text = datetime.now().strftime("%d.%m.%Y %H:%M")
    draw_line(document_title, size=16, extra_gap=4)
    draw_line(f"Сформировано: {now_text}", size=10, extra_gap=8)
    draw_line(f"Внимание: профессии являются примерными и не гарантируют точный прогноз будущего.", size=10, extra_gap=8)

    if not jobs:
        draw_line("Список профессий пуст.", size=12)
    else:
        for index, job in enumerate(jobs, start=1):
            title = job.get("title", "Без названия")
            activity = ", ".join(job.get("activity", []))
            skills = ", ".join(job.get("skills", []))
            why_future = job.get("why_future", "")
            tasks = "; ".join(job.get("tasks", []))
            math_level = job.get("math_level", "")
            communication_level = job.get("communication_level", "")

            draw_line(f"{index}. {title}", size=13, extra_gap=2)
            if activity:
                draw_line(f"Тип деятельности: {activity}")
            if skills:
                draw_line(f"Ключевые навыки: {skills}")
            if why_future:
                draw_line(f"Почему появится: {why_future}")
            if tasks:
                draw_line(f"Типичные задачи: {tasks}")
            if math_level:
                draw_line(f"Уровень математики: {math_level}")
            if communication_level:
                draw_line(f"Уровень коммуникации: {communication_level}")
            draw_line("", extra_gap=6)

    pdf.save()
    buffer.seek(0)
    return buffer.getvalue()


if __name__ == "__main__":
    sample_jobs = [
        {
            "title": "Архитектор цифровых экосистем",
            "activity": ["системный анализ", "проектирование"],
            "skills": ["Python", "анализ данных"],
            "why_future": "Рост сложных цифровых платформ.",
            "tasks": ["Сбор требований", "Проектирование сервисов"],
            "math_level": "средний",
            "communication_level": "высокий",
        }
    ]
    pdf_bytes = build_jobs_pdf_bytes(sample_jobs, "Тестовый экспорт профессий")
    output_path = Path("jobs_export_example.pdf")
    output_path.write_bytes(pdf_bytes)
    print(f"PDF сохранен: {output_path.resolve()}")
