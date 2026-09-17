# Задача 3. group_events — 7/10

Система журналирования хранит события парами `(вид, сообщение)`. Например,
`("error", "timeout")` означает ошибку с сообщением `"timeout"`.

Реализуйте функцию `group_events`. Она возвращает словарь, где ключ — вид
события, а значение — список сообщений этого вида.

## Сигнатура

```python
Event = tuple[str, str]


def group_events(events: list[Event]) -> dict[str, list[str]]: ...
```

## Требования

- сообщения внутри каждой группы сохраняют исходный порядок;
- одинаковые сообщения сохраняются столько раз, сколько встретились;
- ключи словаря идут в порядке первого появления вида события;
- списки сообщений у разных ключей являются разными объектами;
- исходный список событий не изменяется;
- для пустого списка результатом является пустой словарь.

## Примеры

```python
group_events(
    [
        ("info", "started"),
        ("error", "timeout"),
        ("info", "finished"),
    ]
)
# {
#     "info": ["started", "finished"],
#     "error": ["timeout"],
# }

group_events(
    [
        ("warning", "disk"),
        ("warning", "memory"),
        ("warning", "disk"),
    ]
)
# {"warning": ["disk", "memory", "disk"]}

group_events([("z", "one"), ("a", "two"), ("z", "three")])
# {"z": ["one", "three"], "a": ["two"]}

group_events([("info", ""), ("info", "ready")])
# {"info": ["", "ready"]}

group_events([])
# {}
```

Независимость списков означает, что изменение одной готовой группы не меняет
другую:

```python
result = group_events([("a", "same"), ("b", "same")])
result["a"].append("extra")
result["b"]  # ["same"]
```

## Проверка

```bash
uv run pytest seminar03/tasks/task03_group_events -v
```
