# Задача 4. normalize_rows — 7/10

Склад перешёл на записи версии 2, но некоторые источники ещё передают записи
версии 1. Данные уже разобраны в объекты `StockRow(product, quantity, version)`;
`version` по контракту равен 1 или 2, остальные поля корректны. Старую запись
можно преобразовать без потери данных, но о каждом таком случае нужно сообщить.

Реализуйте
`normalize_rows(rows: list[StockRow], *, strict: bool = False) -> tuple[list[StockRow], list[warnings.WarningMessage]]`.

- Сохраните порядок строк. Для каждой записи версии 1 создайте новую запись с
  теми же `product` и `quantity`, но с `version=2`. Записи версии 2 оставьте без
  изменений. Возвращайте новый список и не меняйте входной.
- Для **каждой** записи версии 1 вызовите `warnings.warn` с категорией
  `DeprecationWarning`. Текст должен начинаться с `Строка N:`, где `N` — номер
  строки, начиная с единицы.
  Предупреждение должно указывать на место вызова `normalize_rows` в коде
  вызывающей стороны (`stacklevel=2` при прямом вызове `warn` из функции).
- При `strict=False` соберите и верните все предупреждения в порядке записей
  через `warnings.catch_warnings(record=True)`. Даже если снаружи установлен
  фильтр `ignore`, предупреждение нужно записать для каждой старой строки.
  Для этого внутри контекстного менеджера настройте фильтр `always` для
  `DeprecationWarning`.
- При `strict=True` временно настройте фильтр `error`: первое предупреждение
  версии 1 должно стать исключением `DeprecationWarning`, функция ничего не
  возвращает. Если старых записей нет, верните нормализованные записи и пустой
  список предупреждений.
- После любого исхода восстановите прежнее состояние фильтров предупреждений.
  Предупреждения версии 2 не создавайте.

```python
rows = [StockRow("ручка", 2, 1), StockRow("карандаш", 3, 2)]
normalized, recorded = normalize_rows(rows)
# normalized == [StockRow("ручка", 2, 2), StockRow("карандаш", 3, 2)]
# len(recorded) == 1; recorded[0].category is DeprecationWarning
# rows[0].version == 1

normalize_rows(rows, strict=True)  # поднимает DeprecationWarning
```

## Проверка

```bash
uv run pytest seminar07/tasks/task04_normalize_rows -v
```
