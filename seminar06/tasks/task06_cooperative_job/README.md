# Задача 6. cooperative_job — 10/10

Задание `Job` хранит имя. Наследник `Timed` добавляет ограничение времени,
а `Retried` — число попыток. Нужно объединить эти возможности в одном объекте.

Реализуйте конструкторы трёх классов:

```python
Job(*, name, **kwargs)
Timed(*, timeout, **kwargs)
Retried(*, attempts, **kwargs)
```

Классы, объединяющие возможности, уже объявлены:

```python
class ReliableJob(Timed, Retried):
    pass


class ReverseJob(Retried, Timed):
    pass
```

## Требования

- `Job` сохраняет `name`, `Timed` — `timeout`, `Retried` — `attempts`;
- каждый конструктор принимает свои именованные параметры и передаёт остальные
  дальше через `super()`;
- конструктор `Job` вызывает готовую функцию `register_job(name)` ровно один раз;
- каждый объект регистрируется отдельно, даже если имена совпадают;
- `Timed` и `Retried` работают как по отдельности, так и в обеих комбинациях;
- классы `ReliableJob` и `ReverseJob` остаются пустыми;
- прямые вызовы вроде `Job.__init__(self, ...)` запрещены;
- добавление ещё одного наследника `Job`, который соблюдает эти правила,
  не требует изменения существующих классов.

Функция `register_job` и список `registrations` уже написаны. Менять их и
очищать журнал из конструкторов нельзя. Параметры корректны: имя — строка,
ограничение времени и число попыток — положительные целые. Лишних аргументов
в тестах нет; последнему `object.__init__` передаётся пустой набор аргументов.

## Примеры

```python
registrations.clear()  # начать пример с пустого журнала

job = ReliableJob(name="download", timeout=5, attempts=3)
(job.name, job.timeout, job.attempts)  # ("download", 5, 3)
registrations  # ["download"]

other = ReverseJob(name="upload", timeout=8, attempts=2)
(other.name, other.timeout, other.attempts)  # ("upload", 8, 2)
registrations  # ["download", "upload"]
```

```python
Timed(name="timer", timeout=5).timeout  # 5
Retried(name="retry", attempts=3).attempts  # 3
Job(name="plain").name  # "plain"
```

Перед решением рассмотрите такой вариант конструктора `Timed`:

```python
def __init__(self, *, timeout, **kwargs):
    Job.__init__(self, **kwargs)
    self.timeout = timeout
```

Почему он подходит отдельному `Timed`, но не обеспечивает создание
`ReliableJob`? Выпишите MRO обоих комбинирующих классов и проследите путь
параметров `name`, `timeout` и `attempts`.

## Проверка

```bash
uv run pytest seminar06/tasks/task06_cooperative_job -v
```
