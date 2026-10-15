# Семинары по Python

Практические задачи к курсу Python для направления «Прикладная математика и
информатика». У каждой задачи есть условие, заготовка и тесты.

## Материалы

- [Семинар 1. Базовые типы](seminar01/README.md)
- [Семинар 2. Управляющие конструкции](seminar02/README.md)
- [Семинар 3. Контейнеры](seminar03/README.md)
- [Семинар 4. Ссылки и копирование](seminar04/README.md)
- [Семинар 5. Функции и первые классы](seminar05/README.md)
- [Семинар 6. Классы и специальные методы](seminar06/README.md)
- [Семинар 7. Исключения, предупреждения и контекстные менеджеры](seminar07/README.md)
- [Семинар 8. Протоколы и интерфейсы](seminar08/README.md)
- [Семинар 9. Итераторы и генераторы](seminar09/README.md)
- [Семинар 10. Collections, heapq и itertools](seminar10/README.md)
- [Семинар 11. Замыкания и декораторы](seminar11/README.md)
- [Семинар 12. NumPy и Pandas](seminar12/README.md)

## Подготовка окружения

Установите [uv](https://docs.astral.sh/uv/) и из корня репозитория выполните:

```bash
uv sync --extra test --extra lint
```

Для ноутбука семинара 12 дополнительно нужен набор `notebook`:

```bash
uv sync --extra notebook --extra test --extra lint
```

## Работа с задачей

Откройте README выбранной задачи, реализуйте функции и методы в заготовке
и запустите тесты. Например, для первой задачи семинара 11:

```bash
uv run pytest seminar11/tasks/task01_trimmed -v
```

Все тесты семинара:

```bash
uv run pytest seminar11/tasks -v
```

Для другого семинара замените `seminar11` на его каталог.

Проверка стиля и типов для выбранного семинара:

```bash
uv run ruff check seminar11
uv run mypy seminar11
```

Заготовки вызывают `NotImplementedError`. До решения задачи её тесты падают;
после решения они должны проходить. Тесты менять не нужно.
