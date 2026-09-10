# Семинары по Python

Практические задачи к курсу Python для направления «Прикладная математика и
информатика». Для каждой задачи доступны условие, заготовка функции и публичные
автоматические тесты.

## Материалы

- [Семинар 1. Базовые типы](seminar01/README.md)
- [Семинар 2. Управляющие конструкции](seminar02/README.md)

## Подготовка окружения

Установите [uv](https://docs.astral.sh/uv/) и из корня репозитория выполните:

```bash
uv sync --extra test --extra lint
```

## Работа с задачей

Например, чтобы запустить тесты первой задачи первого семинара:

```bash
uv run pytest seminar01/tasks/task01_seat_position -v
```

Откройте `seminar01/tasks/task01_seat_position/README.md`, реализуйте функцию в
`seat_position.py` и повторяйте запуск, пока все тесты не станут зелёными.

Все тесты выбранного семинара запускаются так:

```bash
uv run pytest seminar01/tasks -v
uv run pytest seminar02/tasks -v
```

Проверить стиль и аннотации типов:

```bash
uv run ruff check .
uv run mypy seminar01 seminar02
```

Заготовки намеренно выбрасывают `NotImplementedError`: до решения задач общий
запуск тестов должен завершаться с ошибками.
