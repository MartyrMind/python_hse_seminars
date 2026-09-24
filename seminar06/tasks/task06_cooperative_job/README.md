# Задача 6. cooperative_job — 10/10

`Job` хранит имя задания. `Timed` добавляет ограничение времени, `Retried` —
число попыток. Реализуйте эти классы так, чтобы возможности работали отдельно
и вместе, при любом из двух порядков наследования.

```python
Timed(name="timer", timeout=5).timeout  # 5
Retried(name="retry", attempts=3).attempts  # 3

a = ReliableJob(name="download", timeout=5, attempts=3)
b = ReverseJob(name="upload", timeout=8, attempts=2)

(a.name, a.timeout, a.attempts)  # ("download", 5, 3)
(b.name, b.timeout, b.attempts)  # ("upload", 8, 2)
```

Классы `ReliableJob(Timed, Retried)` и `ReverseJob(Retried, Timed)` уже объявлены
и остаются пустыми. Базовые классы не должны зависеть от конкретного сочетания
возможностей. Каждый из трёх базовых классов инициализирует только своё поле.
Сигнатуры конструкторов выбирайте самостоятельно.

При каждом создании объекта конструктор `Job` должен один раз вызвать готовую
функцию `register_job(name)`. Менять эту функцию или очищать журнал из классов
нельзя. Все параметры корректны; проверка значений не требуется.

## Проверка

```bash
uv run pytest seminar06/tasks/task06_cooperative_job -v
```
