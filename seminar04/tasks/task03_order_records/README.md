# Задача 3. order_records — 7/10

Результаты участников хранятся в списке записей:

```python
{"group": "A", "score": 10, "name": "Вера"}
```

Записи нужно расположить сначала по группе в алфавитном порядке, а внутри
группы — по убыванию результата. Если группа и результат совпадают, исходный
взаимный порядок записей сохраняется.

Реализуйте две версии операции:

- `ordered_records` возвращает новый список и не меняет исходный;
- `order_records_in_place` переставляет элементы в переданном списке и
  возвращает `None`.

Словари-записи копировать не требуется: новый внешний список содержит те же
объекты записей.

## Сигнатуры

```python
from typing import TypedDict


class Record(TypedDict):
    group: str
    score: int
    name: str


def ordered_records(records: list[Record]) -> list[Record]: ...


def order_records_in_place(records: list[Record]) -> None: ...
```

## Примеры

```python
records = [
    {"group": "B", "score": 8, "name": "Борис"},
    {"group": "A", "score": 7, "name": "Анна"},
    {"group": "A", "score": 10, "name": "Вера"},
    {"group": "B", "score": 9, "name": "Дина"},
]

result = ordered_records(records)
[record["name"] for record in result]
# ["Вера", "Анна", "Дина", "Борис"]

[record["name"] for record in records]
# ["Борис", "Анна", "Вера", "Дина"]

result is records  # False
result[0] is records[2]  # True
```

```python
records = [
    {"group": "A", "score": 10, "name": "первый"},
    {"group": "A", "score": 10, "name": "второй"},
]

[record["name"] for record in ordered_records(records)]
# ["первый", "второй"]
```

```python
records = [
    {"group": "B", "score": 1, "name": "Б"},
    {"group": "A", "score": 2, "name": "А"},
]
alias = records

order_records_in_place(records)  # None
alias is records  # True
[record["name"] for record in alias]  # ["А", "Б"]
```

```python
ordered_records([])  # []
```

## Проверка

```bash
uv run pytest seminar04/tasks/task03_order_records -v
```
