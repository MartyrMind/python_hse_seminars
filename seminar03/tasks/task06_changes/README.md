# Задача 6. changes — 10/10

Настройки приложения прочитали дважды: до перезапуска и после. Нужно построить
словарь изменений. Для каждого затронутого ключа результат содержит одну из
строк:

- `"added"` — ключ появился;
- `"removed"` — ключ исчез;
- `"changed"` — ключ остался, но изменились значение или его точный тип.

Ключи без изменений в результат не входят.

## Сигнатура

```python
Config = dict[str, object]


def changes(before: Config, after: Config) -> dict[str, str]: ...
```

## Требования

- наличие ключа и значение `None` — разные состояния;
- равные значения разных точных типов считаются изменением;
- значение `float("nan")` считается изменившимся, даже если в обоих словарях
  находится один и тот же объект;
- ключи результата идут по алфавиту;
- значения одного ключа поддерживают сравнение через `==` и `!=`, результатом
  сравнения является обычное логическое значение;
- исходные словари и вложенные в них значения не изменяются.

## Примеры

```python
before = {
    "mode": 1,
    "proxy": None,
    "cache": "on",
    "retries": 3,
}

after = {
    "mode": True,
    "proxy": None,
    "timeout": None,
    "retries": 3,
}

changes(before, after)
# {
#     "cache": "removed",
#     "mode": "changed",
#     "timeout": "added",
# }
```

```python
changes({"proxy": None}, {"proxy": None})
# {}

changes({"proxy": None}, {})
# {"proxy": "removed"}

changes({}, {"proxy": None})
# {"proxy": "added"}
```

```python
changes({"mode": 1}, {"mode": True})
# {"mode": "changed"}

changes({"ratio": 1}, {"ratio": 1.0})
# {"ratio": "changed"}
```

```python
nan = float("nan")
changes({"ratio": nan}, {"ratio": nan})
# {"ratio": "changed"}
```

```python
changes({}, {})
# {}

changes({"timeout": 30}, {"timeout": 45})
# {"timeout": "changed"}

changes({"b": 1, "a": 1}, {"c": 1})
# {"a": "removed", "b": "removed", "c": "added"}
```

## Проверка

```bash
uv run pytest seminar03/tasks/task06_changes -v
```
