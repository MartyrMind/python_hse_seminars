# Задача 8 (бонус). render_multiplication_table

Реализуйте функцию `render_multiplication_table(n: int) -> list[str]`,
которая строит таблицу умножения для чисел от 1 до `n`.

Ширина каждой ячейки равна количеству цифр в `n * n`. Числа выровнены по
правому краю, соседние ячейки разделены одним дополнительным пробелом. Для
`n == 0` верните пустой список.

## Сигнатура

```python
def render_multiplication_table(n: int) -> list[str]: ...
```

## Примеры

```python
render_multiplication_table(3)
# ["1 2 3", "2 4 6", "3 6 9"]

render_multiplication_table(4)
# [
#     " 1  2  3  4",
#     " 2  4  6  8",
#     " 3  6  9 12",
#     " 4  8 12 16",
# ]
```

Аргумент неотрицателен. Используйте вложенные циклы и динамическую ширину поля
в f-строке.

## Проверка

```bash
uv run pytest seminar02/tasks/task08_bonus_render_multiplication_table -v
```
