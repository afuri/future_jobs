"""Разбор пользовательской строки на список значений."""

from __future__ import annotations

import re


def split_custom_values(raw_text: str) -> list[str]:
    """
    Преобразует строку с перечислением значений в очищенный список.

    Args:
        raw_text (str): Исходная строка, значения могут быть разделены запятыми, точкой с запятой или переводом строки.

    Returns:
        list[str]: Список непустых уникальных значений в порядке появления.
    """
    chunks = re.split(r"[,;\n]+", raw_text)
    values: list[str] = []
    seen: set[str] = set()

    for chunk in chunks:
        value = chunk.strip()
        if not value:
            continue
        lowered = value.casefold()
        if lowered in seen:
            continue
        seen.add(lowered)
        values.append(value)

    return values


if __name__ == "__main__":
    print(split_custom_values("AI, Data; Design\nCommunication"))
