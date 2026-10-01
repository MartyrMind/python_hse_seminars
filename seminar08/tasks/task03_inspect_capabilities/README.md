# Задача 3. inspect_capabilities — 7/10

Система получает объекты из сторонних модулей и перед работой с ними строит
диагностический отчёт. У объекта можно спросить, есть ли метод с нужным именем;
можно проверить соответствие абстрактному классу; наконец, можно попробовать
саму операцию. Ответы не всегда совпадают.

В заготовке дан неизменяемый класс `CapabilityReport`. Реализуйте функцию
`inspect_capabilities(value: Any) -> CapabilityReport` и заполните пять полей:

- `has_getitem` — результат `hasattr(value, "__getitem__")`;
- `iterable_abc` — считает ли `collections.abc.Iterable` объект итерируемым;
- `iter_starts` — удалось ли вызвать `iter(value)` без `TypeError`;
- `hashable_abc` — считает ли `collections.abc.Hashable` объект хешируемым;
- `hash_works` — удалось ли вызвать `hash(value)` без `TypeError`.

Для `iter_starts` только получите итератор. Не вызывайте `next()` и не
перебирайте элементы: ошибка при последующем получении элемента находится вне
этой проверки. Для `iter()` и `hash()` обрабатывайте **только `TypeError`**.
Любое другое исключение должно пройти наружу без замены.

Важные случаи расхождения:

- Класс с `__getitem__`, но без `__iter__`, может перебираться через старый
  протокол последовательности, хотя `abc.Iterable` отвечает `False`.
- У кортежа с вложенным списком `abc.Hashable` отвечает `True`, но `hash()`
  вызывает `TypeError`.
- `hasattr` видит метод, записанный в словарь отдельного экземпляра, а
  специальные операции Python ищут метод в классе. Поэтому наличие имени
  `__getitem__` ещё не гарантирует успешный `iter()`.

```python
inspect_capabilities(42)
# CapabilityReport(False, False, False, True, True)

inspect_capabilities([1, 2])
# CapabilityReport(True, True, True, False, False)

inspect_capabilities((1, [2]))
# CapabilityReport(True, True, True, True, False)
```

Задача независима от первых двух: классы `Playlist` и `Deck` импортировать не
нужно.

## Проверка

```bash
uv run pytest seminar08/tasks/task03_inspect_capabilities -v
```
