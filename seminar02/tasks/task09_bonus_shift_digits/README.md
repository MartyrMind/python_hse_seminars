# Задача 9 (бонус). shift_digits

Реализуйте функцию `shift_digits(text: str, shift: int) -> str`. Каждую
ASCII-цифру от `0` до `9` нужно циклически сдвинуть на `shift` позиций,
остальные символы оставить без изменений.

После девятки снова идёт ноль. Сдвиг может быть отрицательным и больше десяти
по модулю.

## Сигнатура

```python
def shift_digits(text: str, shift: int) -> str: ...
```

## Примеры

```python
shift_digits("Meet at 19:58", 3)  # "Meet at 42:81"
shift_digits("Room 0", -1)        # "Room 9"
shift_digits("Code 907", 10)      # "Code 907"
```

Под ASCII-цифрами понимаются только символы от `"0"` до `"9"`. Например,
`"²"` и `"٣"` менять не нужно, хотя некоторые строковые методы Python
считают их цифрами. Используйте `ord`, `chr` и остаток от деления.

## Проверка

```bash
uv run pytest seminar02/tasks/task09_bonus_shift_digits -v
```
