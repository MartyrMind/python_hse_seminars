# Задача 1. duration — 5/10

Напишите класс `Duration(seconds)` для длительности в секундах. Длительности
должны складываться друг с другом и работать с обычным `sum` для непустого
списка. Результат — тоже `Duration`, исходные объекты не меняются.

Число секунд хранится в доступном для чтения поле `seconds`. На вход подаются
неотрицательные целые числа; проверять их не нужно.

```python
intro = Duration(30)
lesson = Duration(90)

(intro + lesson).seconds  # 120
sum([intro, lesson, intro]).seconds  # 150
sum([Duration(0)]).seconds  # 0

(intro.seconds, lesson.seconds)  # (30, 90)
```

## Проверка

```bash
uv run pytest seminar06/tasks/task01_duration -v
```
