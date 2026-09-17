# Задача 1. replace_contents — 5/10

На один список могут одновременно ссылаться разные части программы. Требуется
заменить все его элементы так, чтобы сам объект списка сохранился и новое
содержимое было видно через каждую существующую ссылку на него.

Реализуйте функцию `replace_contents`, которая заменяет содержимое `target`
элементами из `replacement` и ничего не возвращает.

## Сигнатура

```python
def replace_contents(target: list[int], replacement: list[int]) -> None: ...
```

## Требования

- после вызова содержимое `target` совпадает с `replacement`;
- объект `target` остаётся тем же;
- список `replacement` не изменяется;
- `target` и `replacement` могут быть одним объектом;
- функция возвращает `None`.

## Примеры

```python
target = [1, 2, 3]
replace_contents(target, [8, 9])
target  # [8, 9]
```

```python
target = [1, 2, 3]
alias = target
replace_contents(target, [4, 5])

target  # [4, 5]
alias  # [4, 5]
alias is target  # True
```

```python
target = [1, 2]
replace_contents(target, [])
target  # []
```

```python
target = []
replacement = [2, 3]
replace_contents(target, replacement)

target  # [2, 3]
replacement  # [2, 3]
```

```python
target = [1, 2, 3]
replace_contents(target, target)
target  # [1, 2, 3]
```

## Проверка

```bash
uv run pytest seminar04/tasks/task01_replace_contents -v
```
