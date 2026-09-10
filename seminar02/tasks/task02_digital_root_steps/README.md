# Задача 2. digital_root_steps

Будем заменять неотрицательное целое число суммой его десятичных цифр, пока не
останется одна цифра. Получившуюся цифру называют цифровым корнем.

Например:

```text
9875 → 29 → 11 → 2
```

Здесь цифровой корень равен 2, а преобразование выполнено три раза.

Реализуйте функцию
`digital_root_steps(n: int) -> tuple[int, int]`, возвращающую цифровой корень
и количество преобразований.

## Сигнатура

```python
def digital_root_steps(n: int) -> tuple[int, int]: ...
```

## Примеры

```python
digital_root_steps(7)     # (7, 0)
digital_root_steps(38)    # (2, 2): 38 → 11 → 2
digital_root_steps(9875)  # (2, 3)
digital_root_steps(0)     # (0, 0)
```

Аргумент неотрицателен. Основной цикл задачи должен быть записан через
`while`.

## Проверка

```bash
uv run pytest seminar02/tasks/task02_digital_root_steps -v
```
