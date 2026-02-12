"""Инкремент значения rate у профессии в JSON-файле."""

from __future__ import annotations

import json
from pathlib import Path
from threading import Lock

_FILE_LOCK = Lock()



def increment_job_rate_in_file(file_path: str, job_id: int) -> bool:
    """
    Увеличивает значение `rate` у профессии по `job_id` на 1.

    Args:
        file_path (str): Путь до JSON-файла с профессиями.
        job_id (int): Идентификатор профессии.

    Returns:
        bool: `True`, если профессия найдена и обновлена, иначе `False`.
    """
    json_path = Path(file_path)

    with _FILE_LOCK:
        jobs_data = json.loads(json_path.read_text(encoding="utf-8"))
        was_updated = False

        for job in jobs_data:
            if int(job.get("id", 0)) == int(job_id):
                current_rate = int(job.get("rate", 0))
                job["rate"] = current_rate + 1
                was_updated = True
                break

        if was_updated:
            json_path.write_text(
                json.dumps(jobs_data, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )

        return was_updated


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print(
            "Использование: python services/increment_job_rate_in_file.py "
            "<file_path> <job_id>"
        )
    else:
        file_arg = sys.argv[1]
        job_id_arg = int(sys.argv[2])
        result = increment_job_rate_in_file(file_arg, job_id_arg)
        print(f"Обновлено: {result}")
