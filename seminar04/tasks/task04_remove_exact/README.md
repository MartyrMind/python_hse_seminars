# Задача 4. remove_exact — 8/10

В списке могут находиться разные объекты с одинаковым содержимым. Требуется
удалить конкретный переданный объект, не затрагивая другой равный ему объект.

Реализуйте функцию `remove_exact`. Она удаляет первое вхождение именно объекта
`target` и возвращает `True`. Если этого объекта в списке нет, список остаётся
без изменений, а функция возвращает `False`.

## Сигнатура

```python
def remove_exact(items: list[object], target: object) -> bool: ...
```

## Примеры

```python
target = {"name": "same"}
items = [target, "tail"]

remove_exact(items, target)  # True
items  # ["tail"]
```

```python
equal_copy = {"name": "same"}
target = {"name": "same"}
items = [equal_copy, target]

remove_exact(items, target)  # True
len(items)  # 1
items[0] is equal_copy  # True
```

```python
present = [1, 2]
absent = [1, 2]
items = [present]

remove_exact(items, absent)  # False
items[0] is present  # True
```

```python
one = int("1")
flag = True
items = [one, flag]

remove_exact(items, flag)  # True
len(items)  # 1
items[0] is one  # True
```

```python
nan = float("nan")
items = [nan]

remove_exact(items, nan)  # True
items  # []
```

```python
target = []
items = [target, target, "tail"]

remove_exact(items, target)  # True
len(items)  # 2
items[0] is target  # True
```

## Проверка

```bash
uv run pytest seminar04/tasks/task04_remove_exact -v
```
