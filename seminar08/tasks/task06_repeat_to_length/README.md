# Задача 6. repeat_to_length — 10/10

Система собирает объявления и ритмические рисунки из фрагментов разных
библиотек. Фрагмент можно повторить умножением на целое число; число элементов
в нём узнаётся через `len()`. Реализации не имеют общего прикладного родителя.
Готовые `TextFragment` и `BeatFragment` лежат в `fragments.py`: изучите их,
но не меняйте.

Реализуйте в `repeat_to_length.py` структурный интерфейс и две функции.

1. `RepeatableSized(Protocol)` описывает `__len__() -> int` и умножение на
   `int`, результат которого имеет **тот же конкретный тип**, что и объект.
   Для этого можно использовать `typing.Self` или эквивалентную аннотацию
   `self` через `TypeVar`. Сторонним классам наследоваться от протокола не
   нужно. `@runtime_checkable` и проверки `isinstance` здесь не нужны.
2. Ограничьте `TypeVar` протоколом и типизируйте
   `repeat_to_length(value, minimum: int)` так, чтобы результат сохранял
   конкретный тип `value`.
3. `repeat_to_length` выбирает **минимальное положительное** число копий
   `copies`, для которого `copies * len(value) >= minimum`. `minimum` должно
   быть положительным, а исходная длина — ненулевой; иначе вызовите
   `ValueError`. Один раз вычислите `result = value * copies`. Если
   `len(result) != copies * len(value)`, вызовите `RepeatLengthError`.
   Ошибки самого умножения или `len()` проходят наружу без замены.
4. `RepeatLengthError` — наследник `ValueError` с полями `copies`,
   `expected_length` и `actual_length`. Точный текст ошибки не проверяется.
5. `repeat_all(values, minimum: int)` принимает любой `Iterable` таких
   фрагментов, включая генератор, и возвращает список результатов в исходном
   порядке. Сохраните конкретный тип элемента в аннотации `list[...]`.
   Проверяйте `minimum > 0` даже для пустого входа. При ошибке отдельного
   фрагмента прекратите обработку и пропустите то же исключение наружу.

```python
repeat_to_length("ab", 5)              # "ababab", три копии
repeat_to_length("abc", 3)             # "abc", одна копия
repeat_to_length(TextFragment("ab"), 5)
# TextFragment(text="ababab")

repeat_all((TextFragment(s) for s in ["ab", "xyz"]), 5)
# [TextFragment(text="ababab"), TextFragment(text="xyzxyz")]

repeat_to_length("", 5)                # ValueError
repeat_all([], 0)                     # ValueError
```

`Protocol` позволяет анализатору проверить сигнатуры методов, но не закон
роста длины при умножении. Поэтому функция проверяет этот закон во время
выполнения. Публичные тесты проверяют и обычное поведение, и статические типы
через `mypy`: `Any` или возвращаемый тип `RepeatableSized` вместо конкретного
типа аргумента не подходят.

## Проверка

Для этой задачи нужен `mypy` из дополнительной группы `lint`.

```bash
uv sync --extra test --extra lint
uv run pytest seminar08/tasks/task06_repeat_to_length -v
```
